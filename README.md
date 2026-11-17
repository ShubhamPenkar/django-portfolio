# Personal Portfolio & Showcase — Django

A modern, responsive, and secure personal portfolio web application built with **Python**, **Django 5.2**, and modern **CSS3**. Includes dynamic project showcases, an interactive skill arsenal, and an authenticated contact submission and management system.

---

## 🚀 Key Features

* **Dynamic Project Showcase:** Powered by a relational `Project` model with support for tech tags, GitHub repository links, and live demo buttons.
* **Skill Arsenal:** Dynamic `Skill` model rendering proficiency progress bars and category groupings with responsive auto-fit layouts.
* **Robust Contact System:** 
  * Powered by Django `ModelForm` with built-in validation (email syntax, phone formatting, input sanitation).
  * Safe POST processing with form state retention on validation failure.
  * Flash message alert notifications (Success/Error/Warning) with auto-dismissible styling.
  * Django Admin panel for message filtering, searching, and management.
* **Security & Production-Hardened:**
  * Environment variable management via `python-dotenv`.
  * Dedicated `MEDIA_ROOT` isolation (`BASE_DIR / 'media'`).
  * WhiteNoise integration with compressed and manifest static storage.
  * Safe host header handling.
* **Mobile-First Responsive Design:** Clean dark aesthetic with CSS variables and responsive media query breakpoints.
* **Automated Unit Tests:** Full test suite covering views, status codes, form submissions, and model methods.

---

## 🛠 Tech Stack

* **Backend:** Python 3.10+, Django 5.2.3, Gunicorn
* **Database:** SQLite (default for development), PostgreSQL-ready
* **Static Assets:** WhiteNoise 6.9.0
* **Frontend:** Semantic HTML5, CSS3 (Modern Flexbox & CSS Grid), FontAwesome 6, Google Fonts (Outfit)

---

## 📦 Project Structure

```text
django-portfolio/
├── manage.py
├── requirements.txt
├── Procfile
├── .env.example
├── .gitignore
├── README.md
├── personal_portfolio/      # Core Project Configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── pages/                   # Main Portfolio Application
│   ├── models.py            # Contact, Project, and Skill models
│   ├── forms.py             # ModelForm with field validators
│   ├── views.py             # View controllers and fallbacks
│   ├── admin.py             # Admin registration and filters
│   ├── urls.py              # App-level routing
│   ├── tests.py             # Automated unit and view test suite
│   ├── migrations/          # Schema migrations
│   └── templates/           # HTML templates
│       ├── base.html
│       ├── home.html
│       ├── about.html
│       ├── skills.html
│       ├── projects.html
│       └── contact.html
└── static/                  # Static Assets
    └── css/
        └── style.css        # Central stylesheet
```

---

## ⚡ Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/django-portfolio.git
cd django-portfolio
```

### 2. Create and activate a virtual environment
* **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(On Windows: `copy .env.example .env`)*

Adjust values in `.env` as needed:
```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. Create a superuser (to access admin panel)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser. Access the admin dashboard at `http://127.0.0.1:8000/admin/`.

---

## 🧪 Running Tests

To run the automated test suite:
```bash
python manage.py test pages
```

---

## 🌐 Production Deployment

The project includes a `Procfile` configured for Gunicorn:
```text
web: gunicorn personal_portfolio.wsgi
```

When deploying to platforms such as **Render**, **Railway**, or **Heroku**:
1. Set `DJANGO_DEBUG=False`.
2. Generate a fresh, random `DJANGO_SECRET_KEY`.
3. Set `DJANGO_ALLOWED_HOSTS` to your production domain(s).
4. Run `python manage.py collectstatic --noinput`.
5. Run `python manage.py migrate`.

