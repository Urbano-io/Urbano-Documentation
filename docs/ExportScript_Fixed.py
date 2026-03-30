# =============================================================================
# Grasshopper Component Documentation Export Script (FIXED v2)
# =============================================================================
# Copy-paste this into the GH Python script component in GenerateDocumentation.ghx
#
# FIXES APPLIED:
#   1. AddObject(obj, False, 0) — prevents topology-triggered re-solves
#   2. Removed canvas.Refresh() from add/remove helpers — no UI-triggered re-solves
#   3. Removed pre-capture canvas.Refresh() — GenerateHiResImage renders internally
#   4. Removed redundant ExpireLayout/PerformLayout in main loop
#   5. AppDomain-based running guard — persists across script resets
#   6. Diagnostic prints at every decision point for debugging
#   7. TypeName + Access info for input/output parameters in markdown
# =============================================================================

import Grasshopper
import System
import System.Drawing
import System.Drawing.Imaging
import System.Runtime.InteropServices
import System.Collections.Generic
import shutil
import os
import glob
import re
import json
import Rhino

# --- CONFIGURATION -----------------------------------------------------------
# Set to True to wipe the output folder before starting.
CLEAN_OUTPUT_DIR = True

# Set to True to link images with '-crop' suffix (e.g. 'Name-crop.png')
USE_CROPPED_IMAGES = True

# Capture tuning
# We intentionally capture a larger area and trim transparency afterward.
# This is more robust than relying on exact canvas/viewport coordinate sync.
CAPTURE_PADDING = 15
CAPTURE_ZOOM = 1.5
CAPTURE_FRAME_MARGIN_X = 220
CAPTURE_FRAME_MARGIN_Y = 160
TRIM_ALPHA_THRESHOLD = 1
CAPTURE_PIVOT_X = 200
CAPTURE_PIVOT_Y = 215
# -----------------------------------------------------------------------------


# --- RE-ENTRY GUARD (AppDomain-based, survives script resets) ----------------
_GUARD_KEY = "urbano_export_running"
_domain = System.AppDomain.CurrentDomain

def _is_export_running():
    """Check if an export is currently in progress (AppDomain-persisted)."""
    val = _domain.GetData(_GUARD_KEY)
    return val is not None and bool(val)

def _set_export_running(flag):
    """Set the running flag in .NET AppDomain data."""
    _domain.SetData(_GUARD_KEY, flag)

# Force-clear any stale guard from a crashed previous run.
# (If the script is re-evaluated from source, previous run definitely ended.)
# We detect "fresh load" by checking a module-level sentinel.
if not hasattr(_set_export_running, "_loaded"):
    _set_export_running._loaded = True
    if _is_export_running():
        print("[GUARD] Clearing stale running flag from previous crashed run.")
        _set_export_running(False)
# -----------------------------------------------------------------------------


# --- TEXT HELPERS ------------------------------------------------------------
def _read_text_safely(path):
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def _ensure_parent_dir(path):
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

def ensure_utf8_file(path):
    if not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as _f:
            _ = _f.read()
    except UnicodeDecodeError:
        txt = _read_text_safely(path)
        _ensure_parent_dir(path)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)

def write_utf8(path, text, mode="w"):
    _ensure_parent_dir(path)
    with open(path, mode, encoding="utf-8", newline="\n") as f:
        f.write(text)

def clean_string(text):
    if not text: return ""
    text = text.replace("%20", " ")
    text = text.replace("|", " ").replace(":", "").replace("/", "_").replace("\\", "_")
    text = text.replace("<", "").replace(">", "").replace("?", "").replace("*", "").replace("\"", "")
    text = text.replace("(", "").replace(")", "")
    while "  " in text:
        text = text.replace("  ", " ")
    return text.strip()

def should_process_category(cleaned_sub_cat):
    return True

def write_grouped_components(file_path, exposure_dict, link_prefix="components/"):
    main_components = []
    hidden_components = []

    for expo_name in sorted(exposure_dict.keys()):
        comps = sorted(exposure_dict[expo_name])
        if "obscure" in expo_name.lower():
            hidden_components.extend(comps)
        else:
            main_components.extend(comps)

    if main_components:
        write_utf8(file_path, "#### Main Components\n", mode="a")
        for comp in main_components:
            display_name = comp.replace('_', ' ')
            write_utf8(file_path, f"* [{display_name}]({link_prefix}{comp}.md)\n", mode="a")

    if hidden_components:
        write_utf8(file_path, "\n#### Hidden Components\n", mode="a")
        for comp in hidden_components:
            display_name = comp.replace('_', ' ')
            write_utf8(file_path, f"* [{display_name}]({link_prefix}{comp}.md)\n", mode="a")

def reset_output_directories(base_dir):
    if not CLEAN_OUTPUT_DIR:
        print("Skipping directory cleanup (CLEAN_OUTPUT_DIR = False)")
        return
    print(f"Cleaning output directories in {base_dir}...")
    dirs_to_clean = [
        os.path.join(base_dir, "categories"),
        os.path.join(base_dir, "text"),
    ]
    for d in dirs_to_clean:
        if os.path.exists(d):
            try: shutil.rmtree(d)
            except: pass
    comp_dir = os.path.join(base_dir, "components")
    if os.path.exists(comp_dir):
        md_files = glob.glob(os.path.join(comp_dir, "*.md"))
        for f in md_files:
            try: os.remove(f)
            except: pass
# -----------------------------------------------------------------------------


# --- IMAGE HELPERS -----------------------------------------------------------
def trim_transparent_png(src_path, dst_path, pad=0, alpha_threshold=1):
    bmp = System.Drawing.Bitmap(src_path)
    try:
        width = bmp.Width
        height = bmp.Height

        rect = System.Drawing.Rectangle(0, 0, width, height)
        pixel_format = System.Drawing.Imaging.PixelFormat.Format32bppArgb
        data = bmp.LockBits(rect, System.Drawing.Imaging.ImageLockMode.ReadOnly, pixel_format)
        try:
            stride = abs(data.Stride)
            byte_count = stride * height
            buffer = System.Array.CreateInstance(System.Byte, byte_count)
            System.Runtime.InteropServices.Marshal.Copy(data.Scan0, buffer, 0, byte_count)
        finally:
            bmp.UnlockBits(data)

        min_x = width
        min_y = height
        max_x = -1
        max_y = -1

        for y in range(height):
            row_offset = y * stride
            for x in range(width):
                alpha = buffer[row_offset + (x * 4) + 3]
                if alpha >= alpha_threshold:
                    if x < min_x: min_x = x
                    if y < min_y: min_y = y
                    if x > max_x: max_x = x
                    if y > max_y: max_y = y

        if max_x < min_x or max_y < min_y:
            shutil.copyfile(src_path, dst_path)
            return False

        left = max(min_x - pad, 0)
        top = max(min_y - pad, 0)
        right = min(max_x + pad, width - 1)
        bottom = min(max_y + pad, height - 1)

        crop_rect = System.Drawing.Rectangle(left, top, right - left + 1, bottom - top + 1)
        cropped = bmp.Clone(crop_rect, System.Drawing.Imaging.PixelFormat.Format32bppArgb)
        try:
            cropped.Save(dst_path, System.Drawing.Imaging.ImageFormat.Png)
        finally:
            cropped.Dispose()
        return True
    finally:
        bmp.Dispose()
# -----------------------------------------------------------------------------


# --- CAPTURE & EXPORT --------------------------------------------------------
def captureGrasshopperScreen(component, workingDirectory):
    name = getComponentName(component)
    fileName = name + ".png"
    cropFileName = name + "-crop.png"
    print(f"Capturing screenshot for {fileName}...")

    canvas = Grasshopper.Instances.ActiveCanvas
    if canvas is None:
        raise RuntimeError("Active Grasshopper canvas is not available.")

    if component.Attributes is None:
        component.CreateAttributes()
    if component.Attributes is None:
        raise RuntimeError(f"Component '{component.Name}' has no drawable attributes.")

    component.Attributes.ExpireLayout()
    component.Attributes.PerformLayout()

    rect = System.Drawing.Rectangle.Ceiling(component.Attributes.Bounds)
    rect.Inflate(CAPTURE_FRAME_MARGIN_X, CAPTURE_FRAME_MARGIN_Y)

    imageSettings = Grasshopper.GUI.Canvas.GH_Canvas.GH_ImageSettings()
    imageSettings.Zoom = CAPTURE_ZOOM

    # FIX: Removed canvas.Refresh() — GenerateHiResImage renders internally.
    # A Refresh() here triggers a new solve cycle which causes re-entry.

    imgs = canvas.GenerateHiResImage(rect, imageSettings)
    screenCapture = imgs[0][0]

    out_dir = os.path.join(workingDirectory, "images", "components")
    rawPath = os.path.join(out_dir, name + "-raw.png")
    filePath = os.path.join(out_dir, fileName)
    shutil.copyfile(screenCapture, rawPath)
    trim_transparent_png(rawPath, filePath, CAPTURE_PADDING, TRIM_ALPHA_THRESHOLD)

    cropPath = os.path.join(out_dir, cropFileName)
    shutil.copyfile(filePath, cropPath)
    if os.path.exists(rawPath):
        os.remove(rawPath)

    temp_dir = os.path.split(screenCapture)[0]
    if temp_dir and os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)


def remove_component_from_doc(doc, component):
    """Remove component from document WITHOUT triggering a new solve."""
    if doc is None or component is None:
        return
    try:
        matches = [obj for obj in doc.Objects if obj.InstanceGuid == component.InstanceGuid]
        for obj in matches:
            doc.RemoveObject(obj, False)
    except Exception:
        try:
            if component.OnPingDocument() == doc:
                doc.RemoveObject(component, False)
        except Exception:
            pass
    # FIX: Removed canvas.Refresh() — it triggers UI events that chain
    # into new solutions, causing re-entrant execution of this script.


def add_component_to_doc(doc, component):
    """Add component to document WITHOUT triggering a new solve."""
    if doc is None or component is None:
        return

    if component.Attributes is None:
        component.CreateAttributes()

    # FIX: Changed from AddObject(component, True, 0) to False.
    # The True parameter updates document topology, which triggers a full
    # re-solve of every component — including THIS script — causing infinite loops.
    doc.AddObject(component, False, 0)

    try:
        component.Attributes.ExpireLayout()
        component.Attributes.PerformLayout()
    except Exception:
        pass
    # FIX: Removed canvas.Refresh() — same reason as remove_component_from_doc.


def exportIcon(component, pluginName, workingDirectory):
    print(f"Exporting icon for {pluginName}...")
    fileName = getComponentName(component) + ".png"
    filePath = os.path.join(workingDirectory, "images", "icons", fileName)
    icon = component.Icon_24x24
    icon.Save(filePath)


def getComponentByName(document, name):
    print(f"Searching for component: {name}...")
    for component in document.Objects:
        if component.Name == name:
            return component


def getComponentName(component_obj_or_desc):
    raw_name = component_obj_or_desc.Name
    name_no_prefix = raw_name.replace(pluginName + "_", "")
    return clean_string(name_no_prefix).replace(" ", "_")


def get_component_image_filename(name, githubFolder):
    crop_name = f"{name}-crop.png"
    crop_path = os.path.join(githubFolder, "images", "components", crop_name)
    if USE_CROPPED_IMAGES and os.path.exists(crop_path):
        return crop_name
    return f"{name}.png"


def _format_access(access_val):
    """Convert GH_ParamAccess enum to a readable string."""
    s = str(access_val).lower()
    if "list" in s:
        return "list"
    elif "tree" in s:
        return "tree"
    return "item"


def exportDescription(component, pluginName, githubFolder, githubRepo=None):
    originalName = component.Name
    bName = originalName.replace(pluginName + "_", "")
    name = getComponentName(component)
    description = component.Description

    components_dir = os.path.join(githubFolder, "components")
    os.makedirs(components_dir, exist_ok=True)

    lines = []
    header = f"# ![{bName} icon](../images/icons/{name}.png) {bName}"
    if githubRepo:
        source = f" - [[source code]]({githubRepo}/{originalName.replace(' ', '%20')}.cs)\n"
        lines.append(header + source)
    else:
        lines.append(header + "\n")

    image_filename = get_component_image_filename(name, githubFolder)
    image = f"![{bName} component](../images/components/{image_filename})"
    lines.append(image)

    desc = description.split("Provided by ")[0].replace("\n", " ")
    lines.append("\n" + desc)

    try:
        lines.append("\n#### Input")
        for i in range(component.Params.Input.Count):
            param = component.Params.Input[i]
            iname = param.NickName.strip()
            cleaned_description = param.Description.replace("\n", " ")

            # Get type and access info
            try:
                type_name = param.TypeName
            except Exception:
                type_name = ""
            try:
                access = _format_access(param.Access)
            except Exception:
                access = "item"

            # Strip the empty [] that GH appends to NickName for list params,
            # then fill brackets with actual TypeName + access info.
            iname = re.sub(r"\s*\[\s*\]\s*$", "", iname)

            if type_name:
                type_tag = f"[{type_name}]" if access == "item" else f"[{type_name} {access}]"
            else:
                type_tag = f"[{access}]" if access != "item" else ""

            lines.append(f"* ##### {iname} {type_tag}".rstrip())
            lines.append(f"  {cleaned_description}")

        lines.append("\n#### Output")
        for i in range(component.Params.Output.Count):
            param = component.Params.Output[i]
            iname = param.NickName.strip()
            cleaned_description = param.Description.replace("\n", " ")

            try:
                type_name = param.TypeName
            except Exception:
                type_name = ""
            try:
                access = _format_access(param.Access)
            except Exception:
                access = "item"

            iname = re.sub(r"\s*\[\s*\]\s*$", "", iname)

            if type_name:
                type_tag = f"[{type_name}]" if access == "item" else f"[{type_name} {access}]"
            else:
                type_tag = f"[{access}]" if access != "item" else ""

            lines.append(f"* ##### {iname} {type_tag}".rstrip())
            lines.append(f"  {cleaned_description}")
    except Exception:
        pass

    fileName = f"{name}.md"
    filePath = os.path.join(components_dir, fileName)
    write_utf8(filePath, "\n".join(lines))
    return True


def getPluginComponents(pluginName):
    components = {}
    doc = Grasshopper.Instances.ActiveCanvas.Document
    for proxy in Grasshopper.Instances.ComponentServer.ObjectProxies:
        if proxy.Obsolete: continue

        cat = proxy.Desc.Category
        subCat = proxy.Desc.SubCategory

        if cat.strip() == pluginName:
            cleanSubCat = clean_string(subCat)
            if not should_process_category(cleanSubCat):
                continue

            if str(proxy.Kind) == "CompiledObject":
                components[proxy.Desc.Name] = proxy.CreateInstance()
            elif str(proxy.Kind) == "UserObject":
                components[proxy.Desc.Name] = Grasshopper.Kernel.GH_UserObject(proxy.Location).InstantiateObject()
            else:
                try:
                    components[proxy.Desc.Name] = proxy.CreateInstance()
                except:
                    print(f"Skipping component {proxy.Desc.Name} (Kind: {proxy.Kind}) - Could not instantiate")
    return components


def get_plugin_version(plugin_name):
    """Extract the plugin's assembly version from Grasshopper.
    
    Tries GH_AssemblyInfo objects first (most reliable), then falls back
    to scanning loaded .NET assemblies for a name match.
    Returns a version string like '2.1.0' or 'unknown'.
    """
    import System.Reflection

    # Method 1: Search GH_AssemblyInfo objects registered with the component server
    try:
        for lib in Grasshopper.Instances.ComponentServer.Libraries:
            if plugin_name.lower() in lib.Name.lower():
                ver = lib.Version
                if ver:
                    return str(ver)
    except Exception:
        pass

    # Method 2: Search loaded .NET assemblies
    try:
        for asm in System.AppDomain.CurrentDomain.GetAssemblies():
            try:
                name = asm.GetName().Name
                if plugin_name.lower() in name.lower():
                    ver = asm.GetName().Version
                    if ver:
                        return f"{ver.Major}.{ver.Minor}.{ver.Build}"
            except Exception:
                continue
    except Exception:
        pass

    return "unknown"


def createFolderStructure(githubFolder):
    os.makedirs(githubFolder, exist_ok=True)
    imagesFolder = os.path.join(githubFolder, "images")
    for sub in ["components", "icons"]:
        os.makedirs(os.path.join(imagesFolder, sub), exist_ok=True)
    for sub in ["categories", "components"]:
        os.makedirs(os.path.join(githubFolder, sub), exist_ok=True)
# -----------------------------------------------------------------------------


# === MAIN EXECUTION ==========================================================
componentsHeights = {}
pluginComponents = {}

githubFolder = workingDir

# --- SIMPLE RUNNING GUARD (no edge trigger needed) ---------------------------
export_is_on = bool(export)
is_running = _is_export_running()

print(f"[EXPORT] export={export_is_on}, running_guard={is_running}")

if not export_is_on:
    print("[EXPORT] Export input is False — doing nothing.")
elif is_running:
    print("[EXPORT] Already running — skipping re-entrant solve.")
else:
    # --- BEGIN EXPORT ---
    _set_export_running(True)
    print("[EXPORT] === Starting export ===")
    try:
        reset_output_directories(githubFolder)
        createFolderStructure(githubFolder)

        doc = Grasshopper.Instances.ActiveCanvas.Document
        components = getPluginComponents(pluginName)
        print(f"[EXPORT] Found {len(components)} components to export.")

        for GHObjectName, GHObject in components.items():
            if GHObject.Attributes is None:
                GHObject.CreateAttributes()
            if GHObject.Attributes is None:
                print(f"[EXPORT] Skipping {GHObjectName}: no component attributes available.")
                continue

            component = GHObject
            cleanSubCat = clean_string(component.SubCategory)

            if not should_process_category(cleanSubCat):
                continue

            name = getComponentName(component)
            print(f"[EXPORT] Processing: {name}")

            try:
                remove_component_from_doc(doc, GHObject)
                GHObject.Attributes.Pivot = System.Drawing.PointF(CAPTURE_PIVOT_X, CAPTURE_PIVOT_Y)
                add_component_to_doc(doc, GHObject)

                # 1. Capture Image
                captureGrasshopperScreen(component, githubFolder)

                # 2. Export Icon
                exportIcon(component, pluginName, githubFolder)

                # 3. Export Description
                exportDescription(component, pluginName, githubFolder, pluginGHRepo)

                # 4. Record Height
                componentsHeights[name] = str(component.Attributes.Bounds.Height)

                # 5. Record for README
                if cleanSubCat not in pluginComponents:
                    pluginComponents[cleanSubCat] = {}

                expo = str(component.Exposure).split(",")[-1].strip()
                if expo not in pluginComponents[cleanSubCat]:
                    pluginComponents[cleanSubCat][expo] = []

                pluginComponents[cleanSubCat][expo].append(name)
                print(f"[EXPORT] Done: {name}")

            except Exception as e:
                print(f"[EXPORT] Error exporting {name}: {str(e)}")
            finally:
                remove_component_from_doc(doc, GHObject)

        # Write component heights JSON
        with open(os.path.join(githubFolder, "images", "componentsHeight.json"), "w", encoding="utf-8") as compHeight:
            json.dump(componentsHeights, compHeight, ensure_ascii=False, indent=4)

        # --- CATEGORY & README GENERATION ---
        finalOutputFolder = githubFolder
        os.makedirs(os.path.join(finalOutputFolder, "categories"), exist_ok=True)
        os.makedirs(os.path.join(finalOutputFolder, "components"), exist_ok=True)

        for cleanSubCat in pluginComponents:
            safeFileName = cleanSubCat.replace(" ", "_")
            categoryFilePath = os.path.join(finalOutputFolder, "categories", f"{safeFileName}.md")
            ensure_utf8_file(categoryFilePath)
            write_utf8(categoryFilePath, f"# {cleanSubCat}\n")
            write_grouped_components(categoryFilePath, pluginComponents[cleanSubCat], link_prefix="../components/")


        summaryPath = os.path.join(finalOutputFolder, "README.md")
        ensure_utf8_file(summaryPath)
        write_utf8(summaryPath, "# Urbano Component list\n")

        for cleanSubCat in sorted(pluginComponents.keys()):
            write_utf8(summaryPath, f"## {cleanSubCat}\n", mode="a")
            write_grouped_components(summaryPath, pluginComponents[cleanSubCat], link_prefix="components/")

        # --- VERSION DETECTION ---
        # Detect plugin version and write to version.txt for CI pipeline
        plugin_version = get_plugin_version(pluginName)
        print(f"[EXPORT] Detected plugin version: {plugin_version}")

        # Determine docs root and write version.txt
        docs_root = os.path.dirname(githubFolder) if os.path.basename(githubFolder) != "docs" else githubFolder
        test_path = githubFolder
        for _ in range(5):  # safety limit
            if os.path.basename(test_path) == "docs":
                docs_root = test_path
                break
            parent = os.path.dirname(test_path)
            if parent == test_path:
                break
            test_path = parent

        version_txt_path = os.path.join(docs_root, "version.txt")
        try:
            write_utf8(version_txt_path, plugin_version)
            print(f"[EXPORT] Written version {plugin_version} to {version_txt_path}")
        except Exception as ve:
            print(f"[EXPORT] Warning: Could not write version.txt: {ve}")

        print(f"[EXPORT] === Export complete! {len(componentsHeights)} components exported. ===")

    except Exception as ex:
        print(f"[EXPORT] FATAL ERROR: {str(ex)}")
    finally:
        _set_export_running(False)
        print("[EXPORT] Running guard cleared.")

a = True
