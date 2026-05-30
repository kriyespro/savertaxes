from django.contrib import admin
from .models import Tool


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_featured', 'is_active', 'sort_order']
    list_filter = ['category', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active', 'sort_order']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name', 'slug']
