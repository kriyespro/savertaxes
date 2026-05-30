from django.urls import path
from . import views

app_name = 'control'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('leads/', views.CALeadListView.as_view(), name='leads'),
]
