from django.urls import path
from . import views

app_name = 'gst'

urlpatterns = [
    path('', views.GSTIndexView.as_view(), name='index'),
]
