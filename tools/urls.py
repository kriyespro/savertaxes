from django.urls import path
from . import views

app_name = 'tools'

urlpatterns = [
    path('', views.ToolIndexView.as_view(), name='index'),
    path('<slug:slug>/', views.ToolDetailView.as_view(), name='detail'),
    path('<slug:slug>/calc/', views.ToolCalculateView.as_view(), name='calculate'),
    path('<slug:slug>/rate/', views.ToolRateView.as_view(), name='rate'),
]
