from django.urls import path
from . import views

app_name = 'states'

urlpatterns = [
    path('', views.StateListView.as_view(), name='index'),
    path('<slug:slug>/', views.StateDetailView.as_view(), name='detail'),
]
