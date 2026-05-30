from django.contrib import admin
from .models import Subscriber, CALead


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'user_type', 'subscribed_at', 'is_active']
    list_filter = ['user_type', 'is_active']
    search_fields = ['email', 'name']


@admin.register(CALead)
class CALeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'city', 'query_type', 'source_tool', 'status', 'created_at']
    list_filter = ['query_type', 'status']
    list_editable = ['status']
    search_fields = ['name', 'phone', 'email']
    date_hierarchy = 'created_at'
