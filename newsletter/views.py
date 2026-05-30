from django.views import View
from django.http import HttpResponse
from .models import Subscriber, CALead


class SubscribeView(View):
    def post(self, request):
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()
        if not email or '@' not in email:
            return HttpResponse(
                '<p class="text-red-500 text-sm">Please enter a valid email address.</p>')
        Subscriber.objects.get_or_create(
            email=email, defaults={'name': name})
        return HttpResponse(
            '<p class="text-green-600 font-medium">Subscribed! '
            'Check your inbox for the free tax-saving checklist.</p>')


class CALeadView(View):
    def post(self, request):
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        if not name or not phone:
            return HttpResponse(
                '<p class="text-red-500 text-sm">Name and phone are required.</p>')
        CALead.objects.create(
            name=name,
            email=request.POST.get('email', ''),
            phone=phone,
            city=request.POST.get('city', ''),
            query_type=request.POST.get('query_type', 'other'),
            message=request.POST.get('message', ''),
            source_tool=request.POST.get('source_tool', ''),
        )
        return HttpResponse(
            '<p class="text-green-600 font-medium">A CA will contact you within 24 hours!</p>')
