import datetime
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from tools.models import Tool
from blog.models import Article


def get_next_deadline():
    today = datetime.date.today()
    year = today.year
    deadlines = [
        datetime.date(year, 6, 15),
        datetime.date(year, 9, 15),
        datetime.date(year, 12, 15),
        datetime.date(year + 1, 3, 15),
        datetime.date(year + 1, 7, 31),
    ]
    labels = {
        (6, 15): 'Q1 Advance Tax',
        (9, 15): 'Q2 Advance Tax',
        (12, 15): 'Q3 Advance Tax',
        (3, 15): 'Q4 Advance Tax',
        (7, 31): 'ITR Filing Deadline',
    }
    for d in sorted(deadlines):
        if d >= today:
            label = labels.get((d.month, d.day), 'Tax Deadline')
            return {'date': d, 'label': label,
                    'days_left': (d - today).days}
    return None


class HomeView(TemplateView):
    def get_template_names(self):
        market = getattr(self.request, 'market', 'india')
        if market == 'us':
            return ['pages/us_home.jinja']
        return ['pages/home.jinja']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        market = getattr(self.request, 'market', 'india')

        if market == 'us':
            ctx['featured_tools'] = Tool.objects.filter(
                is_featured=True, is_active=True, market='us').order_by('sort_order')[:6]
            ctx['meta_title'] = 'TaxSaver USA — Free Federal Tax Calculators 2025'
            ctx['meta_description'] = ('Free US federal income tax calculators for 2025. '
                                       'Self-employment tax, refund estimator, capital gains, '
                                       'paycheck calculator and more. IRS-accurate, instant results.')
        else:
            ctx['featured_tools'] = Tool.objects.filter(
                is_featured=True, is_active=True, market='india').order_by('sort_order')[:6]
            ctx['latest_articles'] = Article.objects.published().select_related(
                'author', 'category')[:3]
            ctx['next_deadline'] = get_next_deadline()
            ctx['meta_title'] = 'TaxSaver India — Free Income Tax Calculators FY 2025-26'
            ctx['meta_description'] = ('Free income tax calculators for India FY 2025-26. '
                                       'Old vs New regime comparison, HRA, 80C, GST and 50+ tools.')
        return ctx


class AboutView(TemplateView):
    template_name = 'pages/about.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['meta_title'] = 'About TaxSaver India — Our Mission & Team'
        ctx['meta_description'] = ('TaxSaver India provides free, accurate tax '
                                   'calculators and expert guides for Indian taxpayers.')
        return ctx


class ContactView(TemplateView):
    template_name = 'pages/contact.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['meta_title'] = 'Contact Us — TaxSaver India'
        ctx['meta_description'] = 'Get in touch with the TaxSaver India team.'
        return ctx


class DisclaimerView(TemplateView):
    template_name = 'pages/disclaimer.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['meta_title'] = 'Disclaimer — TaxSaver India'
        ctx['meta_description'] = 'TaxSaver India legal disclaimer and terms of use.'
        return ctx


class PrivacyView(TemplateView):
    template_name = 'pages/privacy.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['meta_title'] = 'Privacy Policy — TaxSaver India'
        ctx['meta_description'] = 'TaxSaver India privacy policy — DPDP Act 2023 compliant.'
        return ctx


def search_view(request):
    q = request.GET.get('q', '').strip()
    tools = []
    articles = []
    if q:
        tools = Tool.objects.filter(
            is_active=True, name__icontains=q)[:5]
        articles = Article.objects.published().filter(
            title__icontains=q)[:5]
    return render(request, 'partials/_search_results.jinja',
                  {'tools': tools, 'articles': articles, 'q': q})


class Budget2025View(TemplateView):
    template_name = 'pages/budget_2025.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['meta_title'] = 'Union Budget 2025 — Income Tax Changes Explained'
        ctx['meta_description'] = ('Key income tax changes in Union Budget 2025: new regime slabs, '
                                   '₹12L rebate, standard deduction ₹75,000, and more. FY 2025-26.')
        ctx['canonical_url'] = self.request.build_absolute_uri()
        return ctx


class USHomeView(TemplateView):
    template_name = 'pages/us_home.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['featured_tools'] = Tool.objects.filter(
            is_featured=True, is_active=True, market='us').order_by('sort_order')[:6]
        ctx['meta_title'] = 'TaxSaver USA — Free US Tax Calculators 2025'
        ctx['meta_description'] = ('Free US federal income tax calculators, '
                                   'self-employment tax, capital gains, and IRS tools for 2025.')
        return ctx


class SetMarketView(View):
    """Saves market preference to session, redirects to appropriate home."""

    def get(self, request):
        market = request.GET.get('market', 'us').lower()
        if market not in ('india', 'us'):
            market = 'us'
        request.session['market_override'] = market
        # Default redirect targets
        default_next = '/in/' if market == 'india' else '/'
        next_url = request.GET.get('next', default_next)
        return redirect(next_url)


def handler404(request, exception):
    return render(request, '404.jinja', status=404)


def handler500(request):
    return render(request, '500.jinja', status=500)
