# Generated for Django 5.2.3

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['-created_at'], 'verbose_name': 'Contact Message', 'verbose_name_plural': 'Contact Messages'},
        ),
        migrations.AddField(
            model_name='contact',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='content',
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=100),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='contact',
            name='number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('image_url', models.URLField(blank=True, help_text='Image URL or static asset path', max_length=500)),
                ('technologies', models.CharField(help_text='Comma-separated (e.g. Python, Django, PostgreSQL)', max_length=200)),
                ('github_url', models.URLField(blank=True)),
                ('live_demo_url', models.URLField(blank=True)),
                ('is_featured', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'ordering': ['order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('proficiency', models.PositiveIntegerField(default=80, help_text='Proficiency percentage (0-100)')),
                ('category', models.CharField(choices=[('backend', 'Backend'), ('frontend', 'Frontend'), ('database', 'Database'), ('tools', 'Tools & Others')], default='backend', max_length=20)),
                ('icon_class', models.CharField(blank=True, help_text="e.g. 'fab fa-python' or 'fas fa-database'", max_length=50)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
                'ordering': ['order', 'name'],
            },
        ),
    ]

