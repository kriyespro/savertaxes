"""
India-specific URL patterns mounted at /in/
Middleware forces request.market='india' for all /in/* paths.
Same views — market filtering handles the rest.
"""
from django.urls import path
from pages import views as page_views
from tools import views as tool_views
from blog import views as blog_views
from gst import views as gst_views
from states import views as state_views
from newsletter import views as nl_views

urlpatterns = [
    path('', page_views.HomeView.as_view(), name='india_home'),

    # India tools
    path('tools/', tool_views.ToolIndexView.as_view()),
    path('tools/<slug:slug>/', tool_views.ToolDetailView.as_view()),
    path('tools/<slug:slug>/calc/', tool_views.ToolCalculateView.as_view()),
    path('tools/<slug:slug>/rate/', tool_views.ToolRateView.as_view()),

    # India blog
    path('blog/', blog_views.ArticleListView.as_view()),
    path('blog/<slug:slug>/', blog_views.ArticleDetailView.as_view()),
    path('blog/<slug:slug>/helpful/', blog_views.ArticleHelpfulView.as_view()),

    # India GST
    path('gst/', gst_views.GSTIndexView.as_view()),

    # India state tax
    path('state-tax/', state_views.StateListView.as_view()),
    path('state-tax/<slug:slug>/', state_views.StateDetailView.as_view()),
]
