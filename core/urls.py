from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from core.sitemaps import ToolSitemap, ArticleSitemap, StaticPageSitemap

admin.site.site_header = 'TaxSaver Admin'
admin.site.site_url = '/'

sitemaps = {
    'tools': ToolSitemap,
    'articles': ArticleSitemap,
    'static': StaticPageSitemap,
}


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /sd/',
        'Disallow: /admin/',
        'Disallow: /users/',
        'Disallow: /newsletter/',
        '',
        f'Sitemap: {request.build_absolute_uri("/sitemap.xml")}',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


urlpatterns = [
    path('sd/', admin.site.urls),
    path('', include('pages.urls', namespace='pages')),
    path('in/', include('core.india_urls')),
    path('tools/', include('tools.urls', namespace='tools')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('state-tax/', include('states.urls', namespace='states')),
    path('gst/', include('gst.urls', namespace='gst')),
    path('users/', include('users.urls', namespace='users')),
    path('admin/', include('control.urls', namespace='control')),
    path('newsletter/', include('newsletter.urls', namespace='newsletter')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
