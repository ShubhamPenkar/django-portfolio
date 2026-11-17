from django.contrib import admin
from .models import Contact, Project, Skill


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'number', 'created_at')
    search_fields = ('name', 'email', 'content')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'technologies', 'is_featured', 'order', 'created_at')
    list_editable = ('is_featured', 'order')
    search_fields = ('title', 'description', 'technologies')
    list_filter = ('is_featured', 'created_at')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency', 'category', 'order')
    list_editable = ('proficiency', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('name',)
