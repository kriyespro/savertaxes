from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('us/', views.USHomeView.as_view(), name='us_home'),
    path('budget/2025/', views.Budget2025View.as_view(), name='budget_2025'),
    path('set-market/', views.SetMarketView.as_view(), name='set_market'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('disclaimer/', views.DisclaimerView.as_view(), name='disclaimer'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('search/', views.search_view, name='search'),
]
