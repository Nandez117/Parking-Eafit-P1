# Documentation: Interface Bootstrap Integration

To comply with **Step 5 (Functional Verification - Interface with Bootstrap)** of the workshop, the Bootstrap framework was integrated into the main view file: `parqueadero/templates/home.html`.

Bootstrap was implemented modularly to preserve the original design (CSS Grid) of the parking lot cards, applying its classes primarily to dynamic and state-dependent components. The implementation is described as follows:

### 1. Framework Import
The official **Bootstrap 5** CDN link was included within the `<head>` tag of the HTML document. This enables the responsive design system and utility classes throughout the entire view.

### 2. "Empty State" Layout
The conditional validation executed when the database is empty (`{% empty %}`) was styled 100% using Bootstrap utility classes. This can be summarized as:

* **Design and Structure:** Used `bg-white` (background), `rounded-4` (rounded corners), and `shadow-sm` (subtle shadow) to provide a modern card appearance.
* **Spacing:** Used `p-5` for wide and even inner padding, and `mb-3` / `mb-2` for vertical spacing between the icon and text elements.
* **Alignment (Flexbox):** Applied `d-flex`, `flex-column`, `align-items-center`, and `justify-content-center` to achieve perfect centering of the message on the screen.
* **Typography and Color:** Utilized `text-muted` and `text-secondary` to apply Bootstrap’s standard gray palette to secondary messages, along with `fw-semibold` and `h5` for title hierarchy.

### 3. Buttons
In the "Help Card" (`help-card`), the "Contact Support" button was refactored to use native Bootstrap button components. The following classes were applied:
* `btn` and `btn-dark` for standard styling and dark coloring.
* `w-100` to ensure the button occupies the full width of its container.
* `d-flex`, `align-items-center`, `justify-content-center`, and `gap-2` to correctly align the SVG icon with the text.
