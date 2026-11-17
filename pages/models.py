from django.db import models
from django.utils import timezone


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    number = models.CharField(max_length=20, blank=True)
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} ({self.email})"


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('database', 'Database'),
        ('tools', 'Tools & Others'),
    ]

    name = models.CharField(max_length=50)
    proficiency = models.PositiveIntegerField(default=80, help_text="Proficiency percentage (0-100)")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='backend')
    icon_class = models.CharField(max_length=50, blank=True, help_text="e.g. 'fab fa-python' or 'fas fa-database'")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return f"{self.name} ({self.proficiency}%)"


class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True, help_text="Image URL or static asset path")
    technologies = models.CharField(max_length=200, help_text="Comma-separated (e.g. Python, Django, PostgreSQL)")
    github_url = models.URLField(blank=True)
    live_demo_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        """Returns list of technologies split by comma."""
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(',') if t.strip()]
