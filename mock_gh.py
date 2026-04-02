import sys
import types
sys.modules['Grasshopper'] = types.ModuleType('Grasshopper')
sys.modules['Rhino'] = types.ModuleType('Rhino')
sys.modules['System'] = types.ModuleType('System')
sys.modules['System.Drawing'] = types.ModuleType('System.Drawing')
sys.modules['System.Drawing.Imaging'] = types.ModuleType('System.Drawing.Imaging')
sys.modules['System.Runtime.InteropServices'] = types.ModuleType('System.Runtime.InteropServices')
sys.modules['System.Collections.Generic'] = types.ModuleType('System.Collections.Generic')

import builtins
builtins.workingDir = "docs/urbano-2"
builtins.export = True
builtins.pluginName = "Urbano"
builtins.pluginGHRepo = "https://github.com/Urbano-io/Urbano2-GH-Templates"
import docs.ExportScript_Fixed
