from django.contrib import admin
from .models import Article, Category, Author


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'published_at', 'fy_applicable']
    list_filter = ['is_published', 'category', 'fy_applicable']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['title', 'slug']
    filter_horizontal = ['related_tools']
    date_hierarchy = 'published_at'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'is_ca']
