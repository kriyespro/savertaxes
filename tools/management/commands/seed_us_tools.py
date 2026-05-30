from django.core.management.base import BaseCommand
from tools.models import Tool

US_TOOLS = [
    {
        'slug': 'us-federal-income-tax-calculator',
        'name': 'Federal Income Tax Calculator 2025',
        'short_desc': 'Calculate your 2025 US federal income tax by filing status. See bracket breakdown, effective rate, and take-home pay.',
        'category': 'us_income',
        'market': 'us',
        'is_featured': True,
        'sort_order': 1,
        'fy_applicable': '2025',
        'meta_title': 'Federal Income Tax Calculator 2025 — Free IRS Tax Estimator',
        'meta_description': 'Free 2025 federal income tax calculator. Enter income and filing status to see exact tax brackets, effective rate, and take-home pay. IRS-accurate.',
    },
    {
        'slug': 'us-tax-refund-estimator',
        'name': 'Tax Refund Estimator 2025',
        'short_desc': 'Find out if you get a refund or owe the IRS. Enter your income and W-2 withholding for an instant estimate.',
        'category': 'us_income',
        'market': 'us',
        'is_featured': True,
        'sort_order': 2,
        'fy_applicable': '2025',
        'meta_title': 'Tax Refund Estimator 2025 — Will You Get a Refund or Owe?',
        'meta_description': 'Free 2025 tax refund estimator. Enter W-2 income and withholding to calculate if you get a refund or owe the IRS. Instant result.',
    },
    {
        'slug': 'us-self-employment-tax-calculator',
        'name': 'Self-Employment Tax Calculator 2025',
        'short_desc': 'Calculate SE tax (15.3%) + federal income tax for 1099 freelancers and independent contractors. Includes quarterly payment schedule.',
        'category': 'us_self_employment',
        'market': 'us',
        'is_featured': True,
        'sort_order': 3,
        'fy_applicable': '2025',
        'meta_title': 'Self-Employment Tax Calculator 2025 — 1099 & Freelancer SE Tax',
        'meta_description': 'Free self-employment tax calculator for 2025. Calculate SE tax (15.3%) + federal income tax for 1099 income. See quarterly estimated payments.',
    },
    {
        'slug': 'us-paycheck-calculator',
        'name': 'Paycheck Calculator 2025 — Take-Home Pay',
        'short_desc': 'Calculate your net take-home pay after federal tax, Social Security, Medicare, and state taxes for any pay frequency.',
        'category': 'us_income',
        'market': 'us',
        'is_featured': True,
        'sort_order': 4,
        'fy_applicable': '2025',
        'meta_title': 'Paycheck Calculator 2025 — Net Take-Home Pay After Tax',
        'meta_description': 'Free paycheck calculator for 2025. Calculate take-home pay after federal tax, Social Security, Medicare, and state taxes. Weekly, biweekly, monthly.',
    },
    {
        'slug': 'us-capital-gains-tax-calculator',
        'name': 'Capital Gains Tax Calculator 2025',
        'short_desc': 'Calculate short-term and long-term capital gains tax on stocks, crypto, and real estate. Includes NIIT (3.8%) check.',
        'category': 'us_investment',
        'market': 'us',
        'is_featured': True,
        'sort_order': 5,
        'fy_applicable': '2025',
        'meta_title': 'Capital Gains Tax Calculator 2025 — Short & Long Term Rates',
        'meta_description': 'Free 2025 capital gains tax calculator. Calculate short-term (ordinary rates) and long-term (0%/15%/20%) tax on stocks, crypto, real estate.',
    },
    {
        'slug': 'us-quarterly-estimated-tax',
        'name': 'Quarterly Estimated Tax Calculator 2025',
        'short_desc': 'Calculate Q1–Q4 estimated tax payments with IRS due dates. For freelancers, self-employed, investors, and anyone without withholding.',
        'category': 'us_self_employment',
        'market': 'us',
        'is_featured': True,
        'sort_order': 6,
        'fy_applicable': '2025',
        'meta_title': 'Quarterly Estimated Tax Calculator 2025 — Q1-Q4 IRS Payments',
        'meta_description': 'Free 2025 quarterly estimated tax calculator. Get exact Q1–Q4 payment amounts and IRS due dates. Includes safe harbor calculation.',
    },
    {
        'slug': 'us-standard-vs-itemized-deduction',
        'name': 'Standard vs Itemized Deduction Calculator 2025',
        'short_desc': 'Find out whether to take the standard deduction or itemize. Includes SALT cap, mortgage interest, charitable, and medical deductions.',
        'category': 'us_deductions',
        'market': 'us',
        'is_featured': True,
        'sort_order': 7,
        'fy_applicable': '2025',
        'meta_title': 'Standard vs Itemized Deduction Calculator 2025 — Which Is Better?',
        'meta_description': 'Free 2025 standard vs itemized deduction calculator. Compare your deductions: mortgage interest, SALT ($10K cap), charitable, medical. Which saves more?',
    },
    {
        'slug': 'us-w4-withholding-guide',
        'name': 'W-4 Withholding Guide 2025',
        'short_desc': 'Understand your W-4 and optimize withholding to avoid a big bill or overpay. Get the right withholding for your situation.',
        'category': 'us_income',
        'market': 'us',
        'is_featured': False,
        'sort_order': 8,
        'fy_applicable': '2025',
        'meta_title': 'W-4 Withholding Calculator Guide 2025 — How to Fill Out W-4',
        'meta_description': 'Free W-4 withholding guide for 2025. Understand how to fill out your W-4 to get the right withholding. Avoid underpaying or overpaying the IRS.',
    },
]


class Command(BaseCommand):
    help = 'Seed US tax tools (Tax Year 2025)'

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for t in US_TOOLS:
            obj, is_new = Tool.objects.update_or_create(
                slug=t['slug'],
                defaults=t,
            )
            if is_new:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(
            f'US tools: {created} created, {updated} updated. Total: {created + updated}'
        ))
