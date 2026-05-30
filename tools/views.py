from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from .models import Tool
from . import services
from . import us_services
from .affiliates import get_affiliate


def _get_int(data, key, default=0):
    try:
        return int(data.get(key, default) or default)
    except (ValueError, TypeError):
        return default


def _get_float(data, key, default=0.0):
    try:
        return float(data.get(key, default) or default)
    except (ValueError, TypeError):
        return default


def _calc_regime_compare(data):
    income = _get_int(data, 'income')
    age_group = data.get('age_group', 'below_60')
    fy = data.get('fy', '2025-26')
    deductions = {
        'sec_80c': _get_int(data, 'sec_80c'),
        'sec_80d_self': _get_int(data, 'sec_80d_self'),
        'sec_80d_parents': _get_int(data, 'sec_80d_parents'),
        'hra_exemption': _get_int(data, 'hra_exemption'),
        'home_loan_interest': _get_int(data, 'home_loan_interest'),
        'nps_extra': _get_int(data, 'nps_extra'),
        'other': _get_int(data, 'other_deductions'),
    }
    return services.compare_regimes(income, age_group, deductions, fy)


def _calc_income_tax(data):
    income = _get_int(data, 'income')
    regime = data.get('regime', 'new')
    age_group = data.get('age_group', 'below_60')
    fy = data.get('fy', '2025-26')
    if regime == 'new':
        return services.calculate_new_regime(income, fy)
    return services.calculate_old_regime(income, age_group, fy=fy)


def _calc_hra(data):
    return services.calculate_hra_exemption(
        basic_salary=_get_int(data, 'basic_salary'),
        hra_received=_get_int(data, 'hra_received'),
        annual_rent=_get_int(data, 'annual_rent'),
        is_metro=data.get('is_metro') == 'true',
    )


def _calc_advance_tax(data):
    return services.calculate_advance_tax(
        annual_tax_liability=_get_int(data, 'annual_tax'),
        tds_deducted=_get_int(data, 'tds_deducted'),
        fy=data.get('fy', '2025-26'),
    )


def _calc_capital_gains(data):
    return services.calculate_capital_gains_equity(
        buy_price=_get_float(data, 'buy_price'),
        sell_price=_get_float(data, 'sell_price'),
        units=_get_float(data, 'units'),
        holding_months=_get_int(data, 'holding_months'),
        fy=data.get('fy', '2025-26'),
    )


def _calc_gst(data):
    return services.calculate_gst(
        amount=_get_float(data, 'amount'),
        rate_pct=_get_float(data, 'rate', 18.0),
        reverse=data.get('reverse') == 'true',
    )


def _calc_44ada(data):
    return services.calculate_presumptive_44ada(
        gross_receipts=_get_int(data, 'gross_receipts'),
        fy=data.get('fy', '2025-26'),
    )


def _calc_80c(data):
    return services.calculate_80c_savings(
        gross_income=_get_int(data, 'income'),
        current_80c_investment=_get_int(data, 'invested'),
        marginal_rate_pct=_get_float(data, 'marginal_rate', 30.0),
        fy=data.get('fy', '2025-26'),
    )


def _calc_ctc(data):
    return services.calculate_ctc_to_takehome(
        ctc=_get_int(data, 'ctc'),
        basic_pct=_get_float(data, 'basic_pct', 40.0),
        hra_pct=_get_float(data, 'hra_pct', 50.0),
        regime=data.get('regime', 'new'),
        age_group=data.get('age_group', 'below_60'),
        fy=data.get('fy', '2025-26'),
    )


def _calc_80d(data):
    return services.calculate_80d_savings(
        premium_self=_get_int(data, 'premium_self'),
        senior_self=data.get('senior_self') == 'true',
        premium_parents=_get_int(data, 'premium_parents'),
        senior_parents=data.get('senior_parents') == 'true',
        preventive_self=_get_int(data, 'preventive_self'),
        preventive_parents=_get_int(data, 'preventive_parents'),
        marginal_rate_pct=_get_float(data, 'marginal_rate', 30.0),
        fy=data.get('fy', '2025-26'),
    )


def _calc_tds_salary(data):
    deductions = {
        'sec_80c': _get_int(data, 'sec_80c'),
        'sec_80d_self': _get_int(data, 'sec_80d_self'),
        'hra_exemption': _get_int(data, 'hra_exemption'),
        'home_loan_interest': _get_int(data, 'home_loan_interest'),
        'nps_extra': _get_int(data, 'nps_extra'),
    }
    return services.calculate_tds_on_salary(
        gross_income=_get_int(data, 'income'),
        regime=data.get('regime', 'new'),
        age_group=data.get('age_group', 'below_60'),
        deductions=deductions,
        fy=data.get('fy', '2025-26'),
    )


def _calc_refund(data):
    deductions = {
        'sec_80c': _get_int(data, 'sec_80c'),
        'sec_80d_self': _get_int(data, 'sec_80d_self'),
        'hra_exemption': _get_int(data, 'hra_exemption'),
        'home_loan_interest': _get_int(data, 'home_loan_interest'),
        'nps_extra': _get_int(data, 'nps_extra'),
    }
    return services.calculate_refund_or_demand(
        gross_income=_get_int(data, 'income'),
        tds_deducted=_get_int(data, 'tds_deducted'),
        advance_tax_paid=_get_int(data, 'advance_tax_paid'),
        regime=data.get('regime', 'new'),
        age_group=data.get('age_group', 'below_60'),
        deductions=deductions,
        fy=data.get('fy', '2025-26'),
    )


def _calc_home_loan(data):
    return services.calculate_home_loan_benefit(
        loan_amount=_get_int(data, 'loan_amount'),
        interest_rate_pct=_get_float(data, 'interest_rate', 8.5),
        loan_tenure_years=_get_int(data, 'tenure_years', 20),
        loan_year=_get_int(data, 'loan_year', 1),
        is_self_occupied=data.get('property_type') != 'let_out',
        marginal_rate_pct=_get_float(data, 'marginal_rate', 30.0),
        fy=data.get('fy', '2025-26'),
    )


def _calc_nps(data):
    return services.calculate_nps_benefit(
        basic_salary=_get_int(data, 'basic_salary'),
        employee_nps=_get_int(data, 'employee_nps'),
        employer_nps_pct=_get_float(data, 'employer_nps_pct', 0.0),
        other_80c=_get_int(data, 'other_80c'),
        marginal_rate_pct=_get_float(data, 'marginal_rate', 30.0),
        fy=data.get('fy', '2025-26'),
    )


def _calc_itr_form(data):
    return services.suggest_itr_form(
        has_salary=data.get('has_salary') == 'true',
        has_capital_gains=data.get('has_capital_gains') == 'true',
        has_business_income=data.get('has_business_income') == 'true',
        has_presumptive=data.get('has_presumptive') == 'true',
        has_foreign_assets=data.get('has_foreign_assets') == 'true',
        is_director=data.get('is_director') == 'true',
        total_income=_get_int(data, 'total_income'),
        has_multiple_houses=data.get('has_multiple_houses') == 'true',
        has_fno=data.get('has_fno') == 'true',
    )


def _calc_80g(data):
    return services.calculate_80g_deduction(
        donation_100pct=_get_int(data, 'donation_100'),
        donation_50pct=_get_int(data, 'donation_50'),
        marginal_rate_pct=_get_float(data, 'marginal_rate', 30.0),
        fy=data.get('fy', '2025-26'),
    )


def _calc_80tta(data):
    return services.calculate_80tta_ttb(
        savings_interest=_get_int(data, 'savings_interest'),
        fd_interest=_get_int(data, 'fd_interest'),
        is_senior_citizen=data.get('is_senior') == 'true',
        marginal_rate_pct=_get_float(data, 'marginal_rate', 30.0),
        fy=data.get('fy', '2025-26'),
    )


def _calc_44ad(data):
    return services.calculate_presumptive_44ad(
        gross_turnover=_get_int(data, 'gross_turnover'),
        is_digital=data.get('is_digital') == 'true',
        fy=data.get('fy', '2025-26'),
    )


def _calc_freelancer(data):
    return services.calculate_freelancer_plan(
        gross_receipts=_get_int(data, 'gross_receipts'),
        regime=data.get('regime', 'new'),
        sec_80c=_get_int(data, 'sec_80c'),
        sec_80d=_get_int(data, 'sec_80d'),
        nps_extra=_get_int(data, 'nps_extra'),
        fy=data.get('fy', '2025-26'),
    )


def _calc_property_gains(data):
    return services.calculate_capital_gains_property(
        buy_price=_get_float(data, 'buy_price'),
        sell_price=_get_float(data, 'sell_price'),
        holding_months=_get_int(data, 'holding_months'),
        fy=data.get('fy', '2025-26'),
    )


def _calc_mf_tax(data):
    return services.calculate_mutual_fund_tax(
        invested=_get_float(data, 'invested'),
        current_value=_get_float(data, 'current_value'),
        holding_months=_get_int(data, 'holding_months'),
        fund_type=data.get('fund_type', 'equity'),
        fy=data.get('fy', '2025-26'),
    )


def _calc_elss_ppf_nps(data):
    return services.compare_elss_ppf_nps(
        annual_investment=_get_int(data, 'annual_investment', 50000),
        years=_get_int(data, 'years', 15),
        marginal_rate_pct=_get_float(data, 'marginal_rate', 30.0),
        fy=data.get('fy', '2025-26'),
    )


def _calc_epf(data):
    return services.calculate_epf_maturity(
        basic_salary=_get_int(data, 'basic_salary'),
        years_of_service=_get_int(data, 'years', 10),
        epf_rate=_get_float(data, 'epf_rate', 8.25),
    )


def _calc_ppf(data):
    return services.calculate_ppf_maturity(
        annual_investment=_get_int(data, 'annual_investment'),
        years=_get_int(data, 'years', 15),
        ppf_rate=_get_float(data, 'ppf_rate', 7.1),
    )


def _calc_gratuity(data):
    return services.calculate_gratuity(
        basic_da_salary=_get_int(data, 'basic_da_salary'),
        years_of_service=_get_int(data, 'years_of_service'),
        is_govt=data.get('is_govt') == 'true',
    )


def _calc_senior_tax(data):
    return services.calculate_senior_citizen_tax(
        gross_income=_get_int(data, 'income'),
        age_group=data.get('age_group', '60_to_79'),
        fd_interest=_get_int(data, 'fd_interest'),
        savings_interest=_get_int(data, 'savings_interest'),
        sec_80d=_get_int(data, 'sec_80d'),
        sec_80c=_get_int(data, 'sec_80c'),
        fy=data.get('fy', '2025-26'),
    )


def _calc_surcharge(data):
    return services.calculate_surcharge(
        gross_income=_get_int(data, 'income'),
        regime=data.get('regime', 'new'),
        fy=data.get('fy', '2025-26'),
    )


def _calc_composition(data):
    return services.calculate_gst_composition(
        annual_turnover=_get_int(data, 'annual_turnover'),
        business_type=data.get('business_type', 'trader'),
    )


def _calc_late_fee(data):
    return services.calculate_gstr_late_fee(
        return_type=data.get('return_type', 'GSTR-3B'),
        days_late=_get_int(data, 'days_late'),
        has_tax_liability=data.get('has_liability') != 'false',
        turnover=_get_int(data, 'turnover'),
    )


def _calc_80e(data):
    return services.calculate_80e_benefit(
        annual_interest=_get_int(data, 'annual_interest'),
        loan_year=_get_int(data, 'loan_year', 1),
        marginal_rate_pct=_get_float(data, 'marginal_rate', 30.0),
        fy=data.get('fy', '2025-26'),
    )


def _calc_professional_tax(data):
    return services.calculate_professional_tax(
        annual_income=_get_int(data, 'annual_income'),
        state=data.get('state', 'maharashtra'),
    )


def _calc_nps_vs_epf(data):
    return services.compare_nps_vs_epf(
        basic_salary=_get_int(data, 'basic_salary'),
        years=_get_int(data, 'years', 20),
        marginal_rate_pct=_get_float(data, 'marginal_rate', 30.0),
    )


def _calc_tax_checklist(data):
    return services.generate_tax_checklist(
        gross_income=_get_int(data, 'income'),
        regime=data.get('regime', 'new'),
        has_hra=data.get('has_hra') == 'true',
        sec_80c_invested=_get_int(data, 'sec_80c_invested'),
        has_health_insurance=data.get('has_health_insurance') == 'true',
        has_home_loan=data.get('has_home_loan') == 'true',
        has_nps=data.get('has_nps') == 'true',
        fy=data.get('fy', '2025-26'),
    )


# ── US Calc Functions ────────────────────────────────────────────────

def _us_federal_tax(data):
    return us_services.calculate_federal_tax(
        gross_income=_get_int(data, 'gross_income'),
        filing_status=data.get('filing_status', 'single'),
        use_standard_deduction=data.get('deduction_type', 'standard') == 'standard',
        itemized_deductions=_get_int(data, 'itemized_deductions'),
        num_children=_get_int(data, 'num_children'),
        other_credits=_get_int(data, 'other_credits'),
    )


def _us_se_tax(data):
    return us_services.calculate_se_tax(
        net_profit=_get_float(data, 'net_profit'),
        filing_status=data.get('filing_status', 'single'),
    )


def _us_capital_gains(data):
    return us_services.calculate_capital_gains(
        total_income=_get_int(data, 'total_income'),
        short_term_gain=_get_int(data, 'short_term_gain'),
        long_term_gain=_get_int(data, 'long_term_gain'),
        filing_status=data.get('filing_status', 'single'),
    )


def _us_refund(data):
    return us_services.calculate_tax_refund(
        gross_income=_get_int(data, 'gross_income'),
        total_withholding=_get_int(data, 'total_withholding'),
        filing_status=data.get('filing_status', 'single'),
        use_standard_deduction=data.get('deduction_type', 'standard') == 'standard',
        itemized_deductions=_get_int(data, 'itemized_deductions'),
        num_children=_get_int(data, 'num_children'),
        other_credits=_get_int(data, 'other_credits'),
    )


def _us_quarterly(data):
    return us_services.calculate_quarterly_estimated_tax(
        annual_income=_get_int(data, 'annual_income'),
        filing_status=data.get('filing_status', 'single'),
        is_self_employed=data.get('income_type', 'employee') == 'self_employed',
        prior_year_tax=_get_int(data, 'prior_year_tax'),
    )


def _us_std_vs_itemized(data):
    return us_services.calculate_standard_vs_itemized(
        filing_status=data.get('filing_status', 'single'),
        mortgage_interest=_get_int(data, 'mortgage_interest'),
        state_local_taxes=_get_int(data, 'state_local_taxes'),
        charitable=_get_int(data, 'charitable'),
        medical=_get_int(data, 'medical'),
        gross_income=_get_int(data, 'gross_income'),
        other=_get_int(data, 'other_deductions'),
    )


def _us_paycheck(data):
    return us_services.calculate_paycheck(
        annual_salary=_get_int(data, 'annual_salary'),
        filing_status=data.get('filing_status', 'single'),
        pay_frequency=data.get('pay_frequency', 'biweekly'),
        state_tax_rate=_get_float(data, 'state_tax_rate'),
        pre_tax_401k=_get_int(data, 'pre_tax_401k'),
        pre_tax_hsa=_get_int(data, 'pre_tax_hsa'),
        pre_tax_medical=_get_int(data, 'pre_tax_medical'),
    )


TOOL_CALC_MAP = {
    'old-vs-new-tax-regime': _calc_regime_compare,
    'income-tax-calculator': _calc_income_tax,
    'hra-exemption-calculator': _calc_hra,
    'advance-tax-calculator': _calc_advance_tax,
    'capital-gains-calculator': _calc_capital_gains,
    'gst-calculator': _calc_gst,
    'presumptive-tax-44ada': _calc_44ada,
    '80c-deduction-calculator': _calc_80c,
    'ctc-to-take-home': _calc_ctc,
    '80d-deduction-calculator': _calc_80d,
    'tds-on-salary-calculator': _calc_tds_salary,
    'income-tax-refund-estimator': _calc_refund,
    'home-loan-tax-benefit': _calc_home_loan,
    'nps-tax-benefit-calculator': _calc_nps,
    'which-itr-form-to-file': _calc_itr_form,
    # Phase 2
    '80g-donation-calculator': _calc_80g,
    '80tta-80ttb-calculator': _calc_80tta,
    'presumptive-tax-44ad': _calc_44ad,
    'freelancer-tax-planner': _calc_freelancer,
    'property-capital-gains-calculator': _calc_property_gains,
    'mutual-fund-tax-calculator': _calc_mf_tax,
    'elss-vs-ppf-vs-nps': _calc_elss_ppf_nps,
    'epf-maturity-calculator': _calc_epf,
    'ppf-maturity-calculator': _calc_ppf,
    'gratuity-calculator': _calc_gratuity,
    'senior-citizen-tax-calculator': _calc_senior_tax,
    'surcharge-calculator': _calc_surcharge,
    'gst-composition-calculator': _calc_composition,
    'gstr-late-fee-calculator': _calc_late_fee,
    'section-80e-education-loan': _calc_80e,
    'professional-tax-calculator': _calc_professional_tax,
    'nps-vs-epf-comparison': _calc_nps_vs_epf,
    'tax-saving-checklist': _calc_tax_checklist,
    # US Tools
    'us-federal-income-tax-calculator': _us_federal_tax,
    'us-self-employment-tax-calculator': _us_se_tax,
    'us-capital-gains-tax-calculator': _us_capital_gains,
    'us-tax-refund-estimator': _us_refund,
    'us-quarterly-estimated-tax': _us_quarterly,
    'us-standard-vs-itemized-deduction': _us_std_vs_itemized,
    'us-paycheck-calculator': _us_paycheck,
}


@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60 * 10), name='dispatch')
class ToolIndexView(ListView):
    model = Tool
    template_name = 'tools/tools_index.jinja'
    context_object_name = 'tools'

    def get_queryset(self):
        market = getattr(self.request, 'market', 'india')
        qs = Tool.objects.filter(is_active=True, market=market)
        cat = self.request.GET.get('category')
        if cat and cat != 'all':
            qs = qs.filter(category=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['active_category'] = self.request.GET.get('category', 'all')
        market = getattr(self.request, 'market', 'india')
        if market == 'us':
            ctx['meta_title'] = 'Free US Tax Calculators & Tools 2025'
            ctx['meta_description'] = ('Free US federal income tax, self-employment tax, '
                                       'capital gains, and IRS calculators for 2025.')
        else:
            ctx['meta_title'] = 'Free Indian Tax Calculators & Tools FY 2025-26'
            ctx['meta_description'] = ('50+ free income tax, GST, HRA, and capital gains '
                                       'calculators for FY 2025-26. Updated for Budget 2025.')
        return ctx


class USToolIndexView(ToolIndexView):
    """Alias for ToolIndexView that forces market=us regardless of geo."""
    def get_queryset(self):
        qs = Tool.objects.filter(is_active=True, market='us')
        cat = self.request.GET.get('category')
        if cat and cat != 'all':
            qs = qs.filter(category=cat)
        return qs


@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60 * 10), name='dispatch')
class ToolDetailView(DetailView):
    model = Tool
    template_name = 'tools/tool_detail.jinja'
    context_object_name = 'tool'

    def get_queryset(self):
        return Tool.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['related_tools'] = Tool.objects.filter(
            category=self.object.category, is_active=True
        ).exclude(pk=self.object.pk)[:4]
        ctx['meta_title'] = self.object.meta_title
        ctx['meta_description'] = self.object.meta_description
        ctx['canonical_url'] = self.request.build_absolute_uri()
        return ctx


class ToolCalculateView(View):
    def post(self, request, slug):
        calc_fn = TOOL_CALC_MAP.get(slug)
        if not calc_fn:
            return render(request, 'partials/_tool_result.jinja',
                          {'error': 'Calculator not found for this tool.'})
        try:
            result = calc_fn(request.POST)
            market = getattr(request, 'market', 'india')
            affiliate = get_affiliate(slug, market)
            return render(request, 'partials/_tool_result.jinja',
                          {'result': result, 'slug': slug, 'affiliate': affiliate})
        except (ValueError, TypeError, KeyError):
            return render(request, 'partials/_tool_result.jinja',
                          {'error': 'Please check your inputs and try again.'})


class ToolRateView(View):
    def post(self, request, slug):
        tool = get_object_or_404(Tool, slug=slug, is_active=True)
        vote = request.POST.get('vote')
        if vote == 'up':
            Tool.objects.filter(pk=tool.pk).update(rating_up=tool.rating_up + 1)
        elif vote == 'down':
            Tool.objects.filter(pk=tool.pk).update(rating_down=tool.rating_down + 1)
        tool.refresh_from_db()
        return render(request, 'partials/_tool_rating.jinja', {'tool': tool})
