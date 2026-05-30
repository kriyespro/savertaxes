from django.core.management.base import BaseCommand
from tools.models import Tool


TOOLS = [
    {
        'slug': 'old-vs-new-tax-regime',
        'name': 'Old vs New Tax Regime Calculator',
        'short_desc': 'Compare Old and New tax regimes side-by-side. Find which saves you more for FY 2025-26.',
        'category': 'regime',
        'is_featured': True,
        'sort_order': 1,
        'meta_title': 'Old vs New Tax Regime Calculator FY 2025-26 — Which Is Better?',
        'meta_description': 'Free Old vs New tax regime comparison calculator for FY 2025-26. Enter your income and deductions to find which regime saves you more tax.',
    },
    {
        'slug': 'income-tax-calculator',
        'name': 'Income Tax Calculator FY 2025-26',
        'short_desc': 'Calculate your income tax for FY 2025-26 under Old or New regime with full slab breakdown.',
        'category': 'income',
        'is_featured': True,
        'sort_order': 2,
        'meta_title': 'Income Tax Calculator FY 2025-26 (AY 2026-27) — Free India',
        'meta_description': 'Free income tax calculator for India FY 2025-26. Calculate tax under Old or New regime, see slab breakdown, effective rate and take-home salary.',
    },
    {
        'slug': 'hra-exemption-calculator',
        'name': 'HRA Exemption Calculator',
        'short_desc': 'Calculate your HRA (House Rent Allowance) exemption for FY 2025-26. Metro and non-metro.',
        'category': 'deductions',
        'is_featured': True,
        'sort_order': 3,
        'meta_title': 'HRA Exemption Calculator FY 2025-26 — Free India',
        'meta_description': 'Calculate exact HRA exemption under Section 10(13A) for FY 2025-26. Instant result for metro and non-metro cities.',
    },
    {
        'slug': 'advance-tax-calculator',
        'name': 'Advance Tax Calculator FY 2025-26',
        'short_desc': 'Calculate your advance tax installments for FY 2025-26 with exact due dates and amounts.',
        'category': 'income',
        'is_featured': True,
        'sort_order': 4,
        'meta_title': 'Advance Tax Calculator FY 2025-26 — Due Dates & Amounts',
        'meta_description': 'Free advance tax calculator for FY 2025-26. Get exact installment amounts for Jun 15, Sep 15, Dec 15, and Mar 15 due dates.',
    },
    {
        'slug': '80c-deduction-calculator',
        'name': 'Section 80C Investment Planner',
        'short_desc': 'Find how much more you can invest under 80C and how much tax you will save.',
        'category': 'deductions',
        'is_featured': True,
        'sort_order': 5,
        'meta_title': 'Section 80C Deduction Calculator FY 2025-26 — Free',
        'meta_description': 'Calculate remaining 80C limit and potential tax savings. Covers PPF, ELSS, LIC, EPF, home loan principal and more.',
    },
    {
        'slug': 'gst-calculator',
        'name': 'GST Calculator India',
        'short_desc': 'Calculate GST on any amount at 5%, 12%, 18%, or 28%. Add or reverse GST instantly.',
        'category': 'gst',
        'is_featured': True,
        'sort_order': 6,
        'meta_title': 'GST Calculator India 2025 — Add or Reverse GST Free',
        'meta_description': 'Free GST calculator for India. Calculate GST at 5%, 12%, 18%, 28% or use reverse GST to find original price. Shows CGST and SGST breakup.',
    },
    {
        'slug': 'capital-gains-calculator',
        'name': 'Capital Gains Tax Calculator — Equity & MF',
        'short_desc': 'Calculate STCG and LTCG tax on stocks and mutual funds. Updated for Budget 2024 rates.',
        'category': 'investment',
        'is_featured': True,
        'sort_order': 7,
        'meta_title': 'Capital Gains Tax Calculator India FY 2025-26 — Equity & MF',
        'meta_description': 'Free STCG and LTCG calculator for equity shares and mutual funds. Updated for Budget 2024: STCG 20%, LTCG 12.5% above ₹1.25L.',
    },
    {
        'slug': 'presumptive-tax-44ada',
        'name': 'Presumptive Tax Calculator — Section 44ADA',
        'short_desc': 'Calculate tax under 44ADA presumptive scheme for professionals (CA, doctor, lawyer, consultant).',
        'category': 'freelancer',
        'is_featured': False,
        'sort_order': 8,
        'meta_title': 'Section 44ADA Calculator FY 2025-26 — Presumptive Tax Professionals',
        'meta_description': 'Calculate presumptive tax for professionals under Section 44ADA. For CAs, doctors, lawyers, engineers with receipts up to ₹75 lakhs.',
    },
]


class Command(BaseCommand):
    help = 'Seed initial tax tools'

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for tool_data in TOOLS:
            obj, was_created = Tool.objects.update_or_create(
                slug=tool_data['slug'],
                defaults=tool_data,
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(
            f'Done: {created} tools created, {updated} updated.'))
