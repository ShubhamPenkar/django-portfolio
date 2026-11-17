from django.test import TestCase, Client
from django.urls import reverse
from pages.models import Contact, Project, Skill
from pages.forms import ContactForm


class PagesViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_status_code_and_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_about_page_status_code_and_template(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_skills_page_status_code_and_template(self):
        response = self.client.get(reverse('skills'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'skills.html')
        self.assertIn('skills', response.context)

    def test_projects_page_status_code_and_template(self):
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects.html')
        self.assertIn('projects', response.context)

    def test_contact_page_get_request(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertIsInstance(response.context['form'], ContactForm)


class ContactFormTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_form_valid_submission(self):
        from django.core import mail
        payload = {
            'name': 'Alice Smith',
            'email': 'alice@example.com',
            'number': '9876543210',
            'content': 'I would like to discuss a new Django project.',
        }
        response = self.client.post(reverse('contact'), data=payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Contact.objects.filter(email='alice@example.com').exists())
        contact = Contact.objects.get(email='alice@example.com')
        self.assertEqual(contact.name, 'Alice Smith')
        self.assertContains(response, 'sent successfully')
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Alice Smith', mail.outbox[0].subject)
        self.assertIn('shubhamworks1718@gmail.com', mail.outbox[0].to)

    def test_contact_form_invalid_email(self):
        payload = {
            'name': 'Bob',
            'email': 'not-an-email',
            'number': '1234567890',
            'content': 'Hello world',
        }
        response = self.client.post(reverse('contact'), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Contact.objects.filter(name='Bob').exists())
        self.assertFormError(response.context['form'], 'email', 'Enter a valid email address.')

    def test_contact_form_short_name(self):
        payload = {
            'name': 'A',
            'email': 'a@example.com',
            'number': '1234567890',
            'content': 'Valid message content',
        }
        response = self.client.post(reverse('contact'), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Contact.objects.filter(email='a@example.com').exists())


class ModelUnitTests(TestCase):
    def test_contact_str_representation(self):
        contact = Contact.objects.create(
            name='Jane Doe',
            email='jane@example.com',
            number='1234567890',
            content='Test message',
        )
        self.assertEqual(str(contact), 'Jane Doe (jane@example.com)')

    def test_skill_str_representation(self):
        skill = Skill.objects.create(name='Python', proficiency=90)
        self.assertEqual(str(skill), 'Python (90%)')

    def test_project_str_and_tech_list(self):
        project = Project.objects.create(
            title='Test Portfolio',
            description='A test project',
            technologies='Python, Django, PostgreSQL',
        )
        self.assertEqual(str(project), 'Test Portfolio')
        self.assertEqual(project.tech_list, ['Python', 'Django', 'PostgreSQL'])
