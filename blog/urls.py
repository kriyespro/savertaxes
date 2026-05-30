from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='index'),
    path('category/<slug:category>/', views.ArticleListView.as_view(), name='category'),
    path('<slug:slug>/', views.ArticleDetailView.as_view(), name='detail'),
    path('<slug:slug>/helpful/', views.ArticleHelpfulView.as_view(), name='helpful'),
]
