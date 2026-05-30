from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from django.contrib.auth import get_user_model
from django.shortcuts import render
from newsletter.models import CALead
from tools.models import Tool

User = get_user_model()


@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'control/dashboard.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_users'] = User.objects.count()
        ctx['total_tools'] = Tool.objects.filter(is_active=True).count()
        ctx['new_leads_today'] = CALead.objects.filter(
            created_at__date=__import__('datetime').date.today()).count()
        ctx['total_leads'] = CALead.objects.count()
        ctx['meta_title'] = 'Mission Control — TaxSaver'
        return ctx


@method_decorator(staff_member_required, name='dispatch')
class UserListView(ListView):
    template_name = 'control/users.jinja'
    context_object_name = 'users'
    paginate_by = 50

    def get_queryset(self):
        qs = User.objects.all().order_by('-date_joined')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(email__icontains=q) | qs.filter(username__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['meta_title'] = 'Users — Mission Control'
        return ctx


@method_decorator(staff_member_required, name='dispatch')
class CALeadListView(ListView):
    template_name = 'control/ca_leads.jinja'
    context_object_name = 'leads'
    paginate_by = 50

    def get_queryset(self):
        return CALead.objects.all().order_by('-created_at')
