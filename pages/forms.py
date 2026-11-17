import re
from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'number', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name...',
                'class': 'form-input',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'you@example.com',
                'class': 'form-input',
                'autocomplete': 'email',
            }),
            'number': forms.TextInput(attrs={
                'placeholder': 'Phone number (optional)',
                'class': 'form-input',
                'autocomplete': 'tel',
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Say hello or describe your project...',
                'rows': 5,
                'class': 'form-textarea',
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name

    def clean_number(self):
        number = self.cleaned_data.get('number', '').strip()
        if number:
            digits_only = re.sub(r'[\s\-\+\(\)]', '', number)
            if not digits_only.isdigit() or len(digits_only) < 7:
                raise forms.ValidationError("Please provide a valid phone number (at least 7 digits).")
        return number

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if len(content) < 5:
            raise forms.ValidationError("Message must be at least 5 characters long.")
        return content

