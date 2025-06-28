from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from pages import models
from pages.models import Contact

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def skills(request):
    return render(request, 'skills.html')

def projects(request):
    return render(request, 'projects.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        content = request.POST.get('content')

        if len(name) < 2 or len(name) > 30:
            messages.error(request, 'Name should be between 2 and 30 characters')
            return redirect('contact')

        if len(email) < 3 or len(email) > 50:
            messages.error(request, 'Invalid email')
            return redirect('contact')

        if len(number) < 10 or len(number) > 12:
            messages.error(request, 'Invalid phone number')
            return redirect('contact')

        ins = models.Contact(name=name, email=email, content=content, number=number)
        ins.save()
        messages.success(request, 'Thank you! Your message was submitted.')
        return redirect('contact')

    return render(request, 'contact.html')
