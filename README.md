# Parking-Eafit-P1
# EAFIT Parking – Monitoring System

This project was developed using **Django** as part of the **Project 1** course at **EAFIT University**.  
The system helps to manage and monitor parking information and creates a solid base for future features like vehicle control, data visualization, and administration.

---

## 📌 Project Description

**EAFIT Parking** is a web application built with **Python and Django**.  
Its main goal is to show and organize information about the university parking system.

At this moment, the project includes:
- Basic Django project structure
- A main app called `monitoreo`
- An initial dashboard page
- A working project configuration

---

## 🛠️ Technologies Used

- **Python 3**
- **Django**
- **HTML**
- **SQLite3**
- **GitHub**

---

## 🚀 Development & Methodology

This project follows the **Trunk-Based Development** methodology. All new features are implemented in individual branches before being integrated into the project.

For the **Individual Assignment #2**, the focus was on implementing a specific User Story with full database integration.

### 📖 User Story Implementation
- **US 03 – Parking Lot Status Monitoring**: Full implementation of the real-time monitoring dashboard connected to the SQLite database.
- **Key Features**: Django ORM queries, Bootstrap 5 styling, and asynchronous data update.

👉 **[View Full US-03 Documentation in the Wiki](https://github.com/Nandez117/Parking-Eafit-P1/wiki/Taller-2)**

---

## 📂 Project Structure

EafitParking/
│
├── config/                 # Main Django configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── monitoreo/              # Main application
│   ├── migrations/
│   ├── static/
│   │   └── styles.css
│   ├── templates/
│   │   └── dashboard.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── tests.py
│
├── db.sqlite3              # Database
├── manage.py               # Main project file
└── venv/                   # Virtual environment

---

## 👩‍💻 Author

**Isabella Ocampo Sánchez**  
EAFIT University – Systems Engineering

---

## 📌 Project Status

- Dashboard is working
- Shows available and occupied parking spaces
- Django project structure is correctly set

---

## ▶️ How to Run the Project

1. Clone the repository
```bash
git clone <REPOSITORY_URL>
cd EafitParking
venv\Scripts\activate
pip install django
python manage.py runserver
