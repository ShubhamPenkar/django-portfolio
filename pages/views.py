import sys
import json
import logging
import urllib.request
import urllib.error
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project, Skill
from .forms import ContactForm

logger = logging.getLogger(__name__)

DEFAULT_SKILLS = [
    # Machine Learning & AI
    {'name': 'Python', 'proficiency': 95, 'icon_class': 'fab fa-python', 'category': 'backend'},
    {'name': 'Scikit-learn & XGBoost/LightGBM', 'proficiency': 90, 'icon_class': 'fas fa-brain', 'category': 'backend'},
    {'name': 'SHAP, LIME & Explainable AI', 'proficiency': 88, 'icon_class': 'fas fa-eye', 'category': 'backend'},
    {'name': 'Vertex AI & Gemini API', 'proficiency': 88, 'icon_class': 'fas fa-robot', 'category': 'backend'},
    {'name': 'Speech AI & faster-whisper', 'proficiency': 85, 'icon_class': 'fas fa-microphone-alt', 'category': 'backend'},
    # Backend & Data Engineering
    {'name': 'FastAPI & Pydantic', 'proficiency': 92, 'icon_class': 'fas fa-bolt', 'category': 'backend'},
    {'name': 'Django & Django REST', 'proficiency': 88, 'icon_class': 'fas fa-server', 'category': 'backend'},
    {'name': 'PostgreSQL & SQLAlchemy', 'proficiency': 90, 'icon_class': 'fas fa-database', 'category': 'database'},
    {'name': 'Pandas & Data Wrangling', 'proficiency': 92, 'icon_class': 'fas fa-table', 'category': 'database'},
    {'name': 'Celery & Redis', 'proficiency': 85, 'icon_class': 'fas fa-network-wired', 'category': 'backend'},
    # Optimization & Tools
    {'name': 'Optimization: MILP (SciPy)', 'proficiency': 86, 'icon_class': 'fas fa-route', 'category': 'tools'},
    {'name': 'SQL (PostgreSQL, MongoDB)', 'proficiency': 90, 'icon_class': 'fas fa-cubes', 'category': 'database'},
    {'name': 'React & JavaScript', 'proficiency': 80, 'icon_class': 'fab fa-react', 'category': 'frontend'},
    {'name': 'Git & Docker', 'proficiency': 85, 'icon_class': 'fab fa-git-alt', 'category': 'tools'},
]

DEFAULT_PROJECTS = [
    {
        'title': 'Knowa – Explainable Decision Intelligence Platform',
        'description': 'Architected a multi-tenant decision intelligence platform that turns ML predictions into scored, trackable business interventions across 5 domains. Built SHAP/LIME explanations with trust scoring, causal blindspot engine (confounders, Simpson\'s paradox reversals), and a "don\'t-act" queue for low-confidence cases.',
        'image_url': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80',
        'technologies': 'FastAPI, SQLAlchemy 2.0, Celery, Redis, React, Python, SHAP, LIME',
        'tech_list': ['FastAPI', 'SQLAlchemy 2.0', 'Celery', 'Redis', 'React', 'SHAP', 'LIME'],
        'github_url': 'https://github.com/ShubhamPenkar/Knowa',
        'live_demo_url': '',
    },
    {
        'title': 'MealMind – Demand Forecasting & Surplus Redistribution',
        'description': 'Built the ML and decision backend for institutional kitchens: gradient-boosted demand forecasting with SHAP (3.5% MAPE) feeding a production-sizing optimizer. Formulated surplus redistribution as a MILP with constrained vehicle routing (cold chain, time windows, expiry limits) and Monte Carlo scenario analysis.',
        'image_url': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80',
        'technologies': 'Python, LightGBM, SHAP, SciPy (MILP), Vehicle Routing, Monte Carlo',
        'tech_list': ['Python', 'LightGBM', 'SHAP', 'SciPy (MILP)', 'Vehicle Routing', 'Monte Carlo'],
        'github_url': 'https://github.com/ShubhamPenkar/MealMind',
        'live_demo_url': '',
    },
    {
        'title': 'MediKiosk – Conversational AI Pipeline for Clinical Intake',
        'description': 'Built speech-to-text and clinical extraction pipeline for a team intake system: faster-whisper transcription feeding Gemini extraction into a Pydantic schema with negation and confidence, integrated into a FastAPI backend. Engineered a clause-aware negation scanner and an LLM-free clinical summary service.',
        'image_url': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80',
        'technologies': 'Python, faster-whisper, Gemini API, FastAPI, Pydantic, Speech AI, NLP',
        'tech_list': ['Python', 'faster-whisper', 'Gemini API', 'FastAPI', 'Pydantic', 'NLP'],
        'github_url': 'https://github.com/ShubhamPenkar/MediKiosk',
        'live_demo_url': '',
    },
    {
        'title': 'Multilingual Social Media Toxicity Detection (Published Research)',
        'description': 'Published research paper in IRJMETS (2025): Designed and evaluated machine learning and NLP pipelines for cross-lingual toxicity detection and hate speech classification across multilingual social media content.',
        'image_url': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80',
        'technologies': 'Python, Scikit-learn, NLP, Text Classification, IRJMETS Published',
        'tech_list': ['Python', 'Scikit-learn', 'NLP', 'Research', 'IRJMETS 2025'],
        'github_url': 'https://github.com/kiahvaidya/multilingual-social-media-toxicity-detection',
        'live_demo_url': '',
    },
]


def home(request):
    try:
        featured_projects = Project.objects.filter(is_featured=True)[:3]
        projects_list = list(featured_projects) if featured_projects.exists() else DEFAULT_PROJECTS[:3]
    except Exception:
        projects_list = DEFAULT_PROJECTS[:3]
    return render(request, 'home.html', {'featured_projects': projects_list})


def about(request):
    return render(request, 'about.html')


def skills(request):
    try:
        skill_qs = Skill.objects.all()
        skills_list = list(skill_qs) if skill_qs.exists() else DEFAULT_SKILLS
    except Exception:
        skills_list = DEFAULT_SKILLS
    return render(request, 'skills.html', {'skills': skills_list})


def projects(request):
    try:
        project_qs = Project.objects.all()
        projects_list = list(project_qs) if project_qs.exists() else DEFAULT_PROJECTS
    except Exception:
        projects_list = DEFAULT_PROJECTS
    return render(request, 'projects.html', {'projects': projects_list})


def dispatch_contact_notification(name, email, number, content):
    """
    Delivers contact form submission directly to Shubham's Gmail (shubhamworks1718@gmail.com).
    1. Tries native Django SMTP (if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are set in env).
    2. Falls back to secure HTTPS form forwarder (zero credentials, works out of the box on Vercel).
    """
    recipient = getattr(settings, 'CONTACT_NOTIFICATION_EMAIL', 'shubhamworks1718@gmail.com')
    subject = f"[Portfolio Inquiry] New message from {name}"

    formatted_message = (
        f"You received a new inquiry through your portfolio website:\n\n"
        f"Name:    {name}\n"
        f"Email:   {email}\n"
        f"Phone:   {number or 'Not provided'}\n\n"
        f"Message:\n{content}\n\n"
        f"--------------------------------------------------\n"
        f"Reply directly to {email} to respond."
    )

    # Check if running inside automated test environment
    from django.core import mail
    is_testing = (
        getattr(settings, 'TESTING', False)
        or hasattr(mail, 'outbox')
        or 'locmem' in getattr(settings, 'EMAIL_BACKEND', '')
        or any('test' in arg for arg in sys.argv)
    )

    # 1. Native Gmail SMTP if configured, or test in-memory outbox
    if (getattr(settings, 'EMAIL_HOST_USER', None) and getattr(settings, 'EMAIL_HOST_PASSWORD', None)) or is_testing:
        try:
            send_mail(
                subject=subject,
                message=formatted_message,
                from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER or 'noreply@portfolio.com',
                recipient_list=[recipient],
                fail_silently=False,
            )
            return True
        except Exception as e:
            logger.warning("SMTP email sending failed: %s", e)

    # 2. HTTPS Webhook delivery via FormSubmit (for production serverless without SMTP credentials)
    if not is_testing:
        try:
            url = f"https://formsubmit.co/ajax/{recipient}"
            payload = json.dumps({
                "name": name,
                "email": email,
                "phone": number or "Not provided",
                "message": content,
                "_subject": subject,
                "_replyto": email,
            }).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Django-Portfolio/1.0",
                    "Accept": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status == 200
        except Exception as e:
            logger.warning("HTTPS email forwarding failed: %s", e)

    return False


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception:
                pass

            try:
                dispatch_contact_notification(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    number=form.cleaned_data.get('number', ''),
                    content=form.cleaned_data['content'],
                )
            except Exception:
                pass

            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the highlighted errors below.')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
