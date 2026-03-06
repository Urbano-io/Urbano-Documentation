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
