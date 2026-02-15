# Parking-Eafit-P1
# Eafit Parking – Sistema de Monitoreo

Proyecto desarrollado en **Django** como parte del curso **Proyecto 1** en la Universidad EAFIT.  
El sistema permite gestionar y monitorear información relacionada con el parqueadero, ofreciendo una base sólida para futuras funcionalidades como control de vehículos, visualización de datos y administración.

---

## 📌 Descripción del Proyecto

**Eafit Parking** es una aplicación web desarrollada con **Python y Django**, cuyo objetivo es centralizar y visualizar información del sistema de parqueaderos de la universidad.  

Actualmente, el proyecto cuenta con:
- Estructura base de un proyecto Django
- Aplicación `monitoreo`
- Plantilla inicial de dashboard
- Configuración funcional del entorno

---

## 🛠️ Tecnologías Utilizadas

- **Python 3**
- **Django**
- **HTML**
- **SQLite3**
- **Git & GitHub**

---

## 📂 Estructura del Proyecto

EafitParking/
│
├── config/ # Configuración principal del proyecto Django
│ ├── settings.py
│ ├── urls.py
│ ├── asgi.py
│ └── wsgi.py
│
├── monitoreo/ # Aplicación principal
│ ├── migrations/
│ ├── templates/
│ │ └── dashboard.html
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── views.py
│ └── tests.py
│
├── db.sqlite3 # Base de datos
├── manage.py # Archivo principal del proyecto
└── venv/ # Entorno virtual


---

👩‍💻 Autora

Isabella Ocampo Sánchez

Universidad EAFIT - Ingeniería de Sistemas

---
📌 Estado del Proyecto

*Dashboard funcional
*Visualización de cupos disponibles y ocupados
*Estructura base de Django correctamente configurada

---
## ▶️ Ejecución del Proyecto

1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd EafitParking
venv\Scripts\activate
pip install django
python manage.py runserver
http://127.0.0.1:8000/




