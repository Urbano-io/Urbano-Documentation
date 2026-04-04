## 2024-05-23 - [Centralizing Video Embed Styles]
**Learning:** Found inline `<style>` blocks for responsive video embeds in markdown files. This prevents global accessibility updates and consistent behavior.
**Action:** Moved styles to global `extra.css` and will watch for other inline styles in future markdown files to centralize them.

## 2024-05-24 - [Enhancing Navigation Clarity]
**Learning:** Text-only links in "grid cards" layouts can be easily missed. Using buttons with directional icons improves visibility and indicates "forward movement" more clearly. Explicitly linking to `index.md` in relative paths ensures consistent navigation behavior across different MkDocs configurations.
**Action:** Converted "Learn more" links to buttons with right-aligned arrows and fixed relative paths.

## 2024-05-25 - [Primary CTA Hierarchy & Descriptive Links]
**Learning:** Using generic text like "Learn more" for adjacent primary calls-to-action on landing pages creates poor visual hierarchy and is confusing for screen reader users trying to distinguish destinations. Highlighting the primary recommended path visually while explicitly describing the destination improves both general UX and accessibility.
**Action:** Replaced generic link texts with specific destinations, added `.md-button--primary` to the recommended path, removed directional icons from secondary paths to de-emphasize them, and updated ARIA labels.

## 2024-05-26 - [External Link Accessibility and UX]
**Learning:** External links should open in a new tab so users do not lose their context within the documentation. When opening a new tab, it's critical to include `target="_blank"` with `rel="noopener noreferrer"` for security, and to notify screen reader users via an `aria-label` (e.g., "(opens in a new tab)"). Redundant icon reading should be prevented with `aria-hidden="true"`.
**Action:** Implemented accessible external link pattern for the LinkedIn announcement bar link and will reuse this pattern for future external links.

## 2024-03-02 - Custom 404 Page Structure
**Learning:** Default MkDocs Material 404 page doesn't have an explicit CTA back to the homepage that's easily identified by screen readers. Extending `main.html` to inject a custom `404.html` allows building a better layout using the theme's default classes (`md-button`).
**Action:** When adding 404 pages to MkDocs applications, always extend `main.html` and include a descriptive "Go to Homepage" button with an appropriate `aria-label`.

## 2024-05-27 - [Legacy Documentation Warning]
**Learning:** Having multiple versions of documentation (e.g., `urbano-1` and `urbano-2`) without clear in-page context can confuse users who land on outdated pages via search engines.
**Action:** Injected a persistent warning admonition on all legacy pages (using Jinja2 conditional `{% if "urbano-1/" in page.url %}` in `docs/overrides/main.html`) to inform users and guide them to the active version.

## 2024-05-28 - [Prominent Legacy Upgrade CTA]
**Learning:** Warning banners on legacy pages with regular inline links for migrating to the new version are often overlooked by users because they blend into the text.
**Action:** Transformed the inline upgrade link in the legacy admonition into a highly visible, primary call-to-action button (`.md-button--primary`) with a clear `aria-label`. Added `.legacy-warning-btn` to centralize CSS instead of using inline styles.

## 2025-02-19 - [404 Empty State Actions]
**Learning:** The default 404 page provided a simple button without actionable guidance or strong visual hierarchy, making the recovery path from a broken link less pleasant.
**Action:** Always provide explicit guidance (e.g. "use the search bar") in empty states, and add a semantically hidden icon (`aria-hidden="true"`) to primary fallback buttons (e.g. the home button) to improve visual clarity without compromising screen reader experiences.

## 2024-05-29 - [Alert Role on Persistent Warnings]
**Learning:** Warning banners (like legacy documentation notices) inserted via HTML overrides are read dynamically by screen readers. Applying `role="alert"` ensures screen readers immediately announce these critical warnings to users as soon as the page loads or updates.
**Action:** Always add `role="alert"` to persistent, page-level warning admonitions injected via HTML overrides.

## 2025-02-19 - [WCAG 2.5.3 Label in Name for Voice Dictation]
**Learning:** Accessible names (`aria-label`) that don't match the visible text of buttons can cause issues for voice dictation users who try to interact with UI elements by speaking their visible text.
**Action:** Always ensure that `aria-label` attributes on text-containing elements exactly match or contain the exact visible text string to comply with WCAG 2.5.3.

## 2025-02-19 - [Keyboard Discoverability in Empty States]
**Learning:** Empty states (like 404 pages) that instruct users to take a specific action (e.g., "use the search bar") provide a better UX when they explicitly teach keyboard shortcuts.
**Action:** When directing users to UI elements that have keyboard shortcuts, include a `<kbd>` tag to indicate the shortcut (e.g., `<kbd>/</kbd>`) to improve discoverability for power users.

## 2025-02-19 - [Missing Image Alt Text Pattern in Component Docs]
**Learning:** Found a systemic pattern across ~125 component documentation markdown files where auto-generated or manually inserted images completely lacked `alt` text (e.g., `![]()`). This creates a significant accessibility barrier, especially for screen reader users trying to identify the UI icons and component representations shown in the images.
**Action:** Implemented a script to auto-populate missing `alt` text using meaningful names derived from the image filenames (e.g., `![Building Population icon](...)`). Will ensure all future automated documentation generation routines include descriptive `alt` text by default.

## 2025-03-15 - [404 Page Recovery Paths & Landing Page Empty States]
**Learning:** Empty states without immediate, explicit actions create friction. For 404 pages, providing only a "Go to Homepage" button forces users to lose their context. For category landing pages (like `urbano-2/index.md`) that only instruct users to "use the sidebar", users are left hunting for navigation menus.
**Action:** 1) Always include a `window.history.back()` action alongside the primary home fallback on 404/error pages to respect the user's journey. 2) Always provide a primary CTA button (e.g., "Start Browsing") on empty landing pages to reduce cognitive load and provide a clear "next step".

## 2025-03-24 - [Tactile Feedback for Buttons]
**Learning:** Found buttons with CSS hover-lift effects (like `.md-button` using `translateY(-2px)`) that lacked a corresponding `active` state. Without an active state, the button remains visually lifted during a click, failing to provide the tactile, "pressed" feedback that users expect from a physical-feeling interaction.
**Action:** Added `.md-button:active` with `translateY(0)` and a slight scale down (`scale(0.97)`) to complete the interaction loop. Will always pair hover-lift effects with active-press effects in the future.

## 2025-05-15 - [Clear External Link Indication]
**Learning:** Found several external links on landing pages (like the GitHub links to Grasshopper templates) that lacked visual indication that they point outside the documentation site. Users might click these expecting to stay within the documentation flow, only to be taken to another site entirely, which can be jarring.
**Action:** Appended the `:material-open-in-new:` icon to external links, especially in prominent lists or cards, to provide visual affordance that the link opens a new tab/external site. Also ensured `target="_blank"`, `rel="noopener noreferrer"`, and a descriptive `aria-label` were added for security and accessibility.

## 2025-05-18 - [Accessible Tooltips on Disabled Buttons]
**Learning:** Setting the `disabled` attribute on a button removes it from the keyboard focus order entirely. This means keyboard and screen reader users cannot access the `title` tooltip that explains *why* the button is disabled.
**Action:** Use `aria-disabled="true"` instead of the `disabled` attribute, remove any `onclick` handlers, and apply the disabled styling via CSS `[aria-disabled="true"]`. This keeps the button in the focus order so its explanatory tooltip remains accessible to all users.

## 2025-05-24 - [Direct Search Access in Empty States]
**Learning:** While instructing users to "use the search bar (press /)" in empty states like 404 pages is helpful, it still requires cognitive load to locate the search bar or recall the keyboard shortcut. Mouse/touch users benefit from a direct, single-tap recovery action.
**Action:** In MkDocs Material, use a `<label for="__search" class="md-button">` to create a prominent button that natively triggers the search overlay. Always include this alongside "Go to Homepage" on error pages to provide multiple intuitive recovery paths.

## 2026-04-03 - [Keyboard Accessibility for Label Buttons]
**Learning:** Using a `<label for="...">` styled as a button (e.g., `.md-button`) provides a great click experience without JavaScript, but labels are natively excluded from the keyboard focus order. This completely breaks keyboard navigation for that "button".
**Action:** When using `<label>` elements as UI buttons, always add `tabindex="0"` to include them in the focus order, and implement an `onkeydown` handler to simulate a click when the `Enter` or `Space` key is pressed.
