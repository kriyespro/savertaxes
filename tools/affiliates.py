"""
Market-aware affiliate configuration.
Each entry: name, cta, url, badge, markets (which tool slugs to show on).
"""

INDIA_AFFILIATES = {
    'cleartax': {
        'name': 'ClearTax',
        'cta': 'File your ITR easily — CA-assisted or self-filing',
        'badge': 'Most Popular',
        'badge_color': 'green',
        'url': '#',  # Replace with actual affiliate URL
        'tools': [
            'old-vs-new-tax-regime', 'income-tax-calculator', 'tds-on-salary-calculator',
            'income-tax-refund-estimator', 'which-itr-form-to-file', 'ctc-to-take-home',
        ],
    },
    'tax2win': {
        'name': 'Tax2Win',
        'cta': 'CA-assisted ITR filing from ₹199',
        'badge': 'Expert Help',
        'badge_color': 'blue',
        'url': '#',
        'tools': [
            'old-vs-new-tax-regime', 'income-tax-calculator', 'freelancer-tax-planner',
            'presumptive-tax-44ada', 'presumptive-tax-44ad',
        ],
    },
    'policybazaar': {
        'name': 'PolicyBazaar',
        'cta': 'Save tax under Section 80D — Compare health plans',
        'badge': 'Save Tax',
        'badge_color': 'purple',
        'url': '#',
        'tools': ['80d-deduction-calculator', 'senior-citizen-tax-calculator'],
    },
    'zerodha_coin': {
        'name': 'Zerodha Coin',
        'cta': 'Invest in ELSS — Save up to ₹46,800 tax under 80C',
        'badge': 'Tax-Free Returns',
        'badge_color': 'amber',
        'url': '#',
        'tools': [
            '80c-deduction-calculator', 'elss-ppf-nps-comparison',
            'ppf-maturity-calculator', 'nps-tax-benefit-calculator',
        ],
    },
    'groww_nps': {
        'name': 'Groww NPS',
        'cta': 'Open NPS account — Extra ₹50,000 deduction under 80CCD(1B)',
        'badge': 'Pension + Tax Save',
        'badge_color': 'teal',
        'url': '#',
        'tools': [
            'nps-tax-benefit-calculator', 'nps-vs-epf-comparison',
            'elss-ppf-nps-comparison',
        ],
    },
}

US_AFFILIATES = {
    'turbotax': {
        'name': 'TurboTax',
        'cta': 'File your federal + state taxes — accuracy guaranteed',
        'badge': 'Most Popular',
        'badge_color': 'green',
        'url': '#',  # Replace with actual affiliate URL
        'tools': [
            'us-income-tax-calculator', 'us-tax-refund-estimator',
            'us-standard-vs-itemized', 'us-w4-calculator',
        ],
    },
    'hrblock': {
        'name': 'H&R Block',
        'cta': 'In-person or online tax filing — trusted since 1955',
        'badge': 'Trusted Brand',
        'badge_color': 'blue',
        'url': '#',
        'tools': [
            'us-income-tax-calculator', 'us-tax-refund-estimator',
        ],
    },
    'freetaxusa': {
        'name': 'FreeTaxUSA',
        'cta': 'Free federal filing, low-cost state — no income limit',
        'badge': 'Free Option',
        'badge_color': 'purple',
        'url': '#',
        'tools': [
            'us-income-tax-calculator', 'us-self-employment-tax-calculator',
        ],
    },
    'keeper': {
        'name': 'Keeper Tax',
        'cta': 'Find write-offs automatically — built for freelancers',
        'badge': 'Freelancer Pick',
        'badge_color': 'amber',
        'url': '#',
        'tools': [
            'us-self-employment-tax-calculator', 'us-quarterly-tax-calculator',
        ],
    },
}

# Default affiliate per tool (shown when no specific match)
INDIA_DEFAULT = 'cleartax'
US_DEFAULT = 'turbotax'


def get_affiliate(slug: str, market: str) -> dict | None:
    """Return best affiliate match for a tool slug + market."""
    if market == 'us':
        affiliates = US_AFFILIATES
        default_key = US_DEFAULT
    else:
        affiliates = INDIA_AFFILIATES
        default_key = INDIA_DEFAULT

    # Find first affiliate that lists this tool
    for aff in affiliates.values():
        if slug in aff.get('tools', []):
            return aff

    # Fall back to default affiliate
    return affiliates.get(default_key)
