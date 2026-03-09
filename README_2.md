# 🚗 Parking EAFIT — Estimated Waiting Time

## User Story

**US-08**

**As a** parking lot user  
**I want** to know the estimated waiting time in the entry queue  
**So that** I can make informed decisions before entering the campus.

### Acceptance Criteria

- The system estimates the waiting time based on vehicular flow.
- The information is displayed clearly to the user.
- The estimation helps the user decide whether to enter the campus or not.

---

## Project Description

This web application allows users to view the **estimated waiting time** at EAFIT campus parking lots in real time.

It is built using **Django** with a custom frontend. The system always displays the three campus parking lots — **Central**, **Ingenieros**, and **Idiomas** — each represented by a dedicated card with its photo, stats, and status. When no data has been entered into the database yet, all values default to **0**, meaning the parking lots are shown with zero queue and zero wait time. As real data is gradually fed into the system (number of vehicles in queue, vehicular flow rate), each card updates automatically to reflect current conditions.

This approach means the interface is always functional and ready — the parking lots are never "missing", they simply show neutral values until measurements are recorded.

The frontend includes:

- Display of the three parking lots with representative images and a live status pill.
- Estimated waiting time in minutes per parking lot, calculated by dividing vehicles in queue by the flow rate (vehicles/min).
- Dynamic color coding (🟢 green / 🟡 yellow / 🔴 red) to reflect congestion levels.
- A **decision hero banner** with an overall recommendation and average wait time across all lots.
- Flow percentage progress bars and vehicle queue statistics per card.
- A context-aware advice chip per card based on the current congestion level.
- A live clock updated every second via JavaScript.

---

## Author

**Isabella Cadavid Posada**

---

## Requirements

- Python 3.x
- Django 4.x or higher
- Modern web browser (Chrome, Firefox, Edge)

---

## How to Run the Project

1. **Clone the repository** and switch to the `IsaC` branch:

```bash
git clone -b IsaC https://github.com/Nandez117/timeparkingproject.git
```

2. **Navigate to the project folder:**

```bash
cd timeparkingproject
```

3. *(Optional but recommended)* **Create a virtual environment:**

```bash
python -m venv venv
```

4. **Activate the virtual environment:**

- Windows:
```bash
venv\Scripts\activate
```
- Linux / Mac:
```bash
source venv/bin/activate
```

5. **Install dependencies:**

```bash
pip install django
```

6. **Run database migrations:**

```bash
python manage.py migrate
```

7. **Start the local server:**

```bash
python manage.py runserver
```

8. Open a web browser and go to:

```
http://127.0.0.1:8000/
```

---

## Documentation: Interface Bootstrap Integration

To comply with **Step 5 (Functional Verification - Interface with Bootstrap)** of the workshop, the Bootstrap framework was integrated into the main view file: `estimatedTime/templates/estimatedTime/estimated_time.html`.

Bootstrap was implemented modularly to preserve the original design (CSS Grid) of the parking lot cards, applying its classes primarily to layout, spacing, and interactive components. Since the core visual identity — the card grid, color levels, typography, and decision banner — is handled by a custom CSS system using CSS custom properties (`:root` variables), Bootstrap complements rather than replaces it, providing standardized utilities where consistency and reusability matter most. The implementation is described as follows:

### 1. Framework Import

The official **Bootstrap 5** CDN link was included within the `<head>` tag of the HTML document. This enables the responsive design system and utility classes throughout the entire view. By loading it via CDN, no local installation is required and the framework is always served from an optimized, cached source.

### 2. "Contact Support" Button

The *"Contactar Soporte"* button inside the **Help Card** (`help-card`) was styled using Bootstrap's native button system. Rather than writing custom button CSS from scratch, Bootstrap handles the base styles, hover states, and focus ring automatically. The implementation can be summarized as:

* **Base styling:** Used `btn` and `btn-dark` for the standard button reset and dark coloring, consistent with the navy brand palette of the view.
* **Width:** Applied `w-100` to make the button span the full width of its container, keeping it visually proportional within the help card.
* **Alignment (Flexbox):** Used `d-flex`, `align-items-center`, `justify-content-center`, and `gap-2` to correctly align the SVG icon with the button label, ensuring a clean and centered layout regardless of content length.

### 3. Navigation Bar Layout

The top navigation bar (`nav-bar`) uses Bootstrap's flexbox utilities to manage the distribution of its three sections — brand logo, navigation tabs, and user controls — in a consistent and responsive way. The implementation can be summarized as:

* **Structure:** Applied `d-flex`, `align-items-center`, and `justify-content-between` to correctly space elements across the full width of the bar.
* **Spacing:** Used `gap-2` between the user icon and logout button in the right-side control group.
* **Responsiveness:** Bootstrap's utilities complement the existing custom CSS breakpoints (`@media`) to maintain proper stacking and alignment on smaller screens without duplicating media query logic.

---

## Template Context Variables

The Django view passes the following context variables to the template:

| Variable | Description |
|---|---|
| `central` | Latest queue record for Parqueadero Central |
| `ing` | Latest queue record for Parqueadero Ingenieros |
| `idiomas` | Latest queue record for Parqueadero Idiomas |
| `lvl_central` / `lvl_ing` / `lvl_idiomas` | Color level string: `green`, `yellow`, or `red` |
| `flow_pct_central` / `flow_pct_ing` / `flow_pct_idiomas` | Flow percentage (0–100) for progress bars |
| `advice_central` / `advice_ing` / `advice_idiomas` | Advice text shown in each card's chip |
| `lvl_banner` | Overall banner color level |
| `avg_wait` | Average estimated wait time (minutes) across all lots |

---

## Color Level Logic

| Wait Time | Level | Meaning |
|---|---|---|
| 0 – 4 min | 🟢 `green` | Free flow — enter without issue |
| 5 – 10 min | 🟡 `yellow` | Moderate flow — consider waiting |
| +10 min | 🔴 `red` | Congested — evaluate another entrance |

---

## Static Files

Representative parking lot photos are stored under:

```
tiempo_espera/static/estimatedTime/
├── central.jpg
├── ingenieria.jpg
└── idiomas.jpg
```

---

© 2026 Universidad EAFIT · Medellín, Colombia
