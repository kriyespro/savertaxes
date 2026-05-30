from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('ca-lead/', views.CALeadView.as_view(), name='ca_lead'),
]
