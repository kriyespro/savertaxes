from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from tools.models import Tool
from blog.models import Article


class ToolSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Tool.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('tools:detail', args=[obj.slug])

    def lastmod(self, obj):
        return None


class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Article.objects.published()

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at


class StaticPageSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.5

    def items(self):
        return [
            'pages:home',
            'pages:budget_2025',
            'blog:index',
            'tools:index',
            'pages:about',
            'pages:contact',
            'pages:disclaimer',
            'pages:privacy',
        ]

    def location(self, item):
        return reverse(item)
