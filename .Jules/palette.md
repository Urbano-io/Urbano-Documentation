## 2024-05-23 - [Centralizing Video Embed Styles]
**Learning:** Found inline `<style>` blocks for responsive video embeds in markdown files. This prevents global accessibility updates and consistent behavior.
**Action:** Moved styles to global `extra.css` and will watch for other inline styles in future markdown files to centralize them.

## 2024-05-24 - [Enhancing Navigation Clarity]
**Learning:** Text-only links in "grid cards" layouts can be easily missed. Using buttons with directional icons improves visibility and indicates "forward movement" more clearly. Explicitly linking to `index.md` in relative paths ensures consistent navigation behavior across different MkDocs configurations.
**Action:** Converted "Learn more" links to buttons with right-aligned arrows and fixed relative paths.

## 2024-05-25 - [Primary CTA Hierarchy & Descriptive Links]
**Learning:** Using generic text like "Learn more" for adjacent primary calls-to-action on landing pages creates poor visual hierarchy and is confusing for screen reader users trying to distinguish destinations. Highlighting the primary recommended path visually while explicitly describing the destination improves both general UX and accessibility.
**Action:** Replaced generic link texts with specific destinations, added `.md-button--primary` to the recommended path, removed directional icons from secondary paths to de-emphasize them, and updated ARIA labels.
