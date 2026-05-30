"""
US Federal Tax Data — Tax Year 2025 (IRS Rev. Proc. 2024-40)
Filing year: 2026
"""

# Tax brackets: (upper_limit, rate). None = no upper limit (top bracket).
BRACKETS = {
    'single': [
        (11925,  0.10),
        (48475,  0.12),
        (103350, 0.22),
        (197300, 0.24),
        (250525, 0.32),
        (626350, 0.35),
        (None,   0.37),
    ],
    'married_jointly': [
        (23850,  0.10),
        (96950,  0.12),
        (206700, 0.22),
        (394600, 0.24),
        (501050, 0.32),
        (751600, 0.35),
        (None,   0.37),
    ],
    'married_separately': [
        (11925,  0.10),
        (48475,  0.12),
        (103350, 0.22),
        (197300, 0.24),
        (250525, 0.32),
        (375800, 0.35),
        (None,   0.37),
    ],
    'head_of_household': [
        (17000,  0.10),
        (64850,  0.12),
        (103350, 0.22),
        (197300, 0.24),
        (250500, 0.32),
        (626350, 0.35),
        (None,   0.37),
    ],
}

STANDARD_DEDUCTION = {
    'single':             15000,
    'married_jointly':    30000,
    'married_separately': 15000,
    'head_of_household':  22500,
}

# Long-term capital gains rates 2025
LTCG_BRACKETS = {
    'single': [
        (48350,  0.00),
        (533400, 0.15),
        (None,   0.20),
    ],
    'married_jointly': [
        (96700,  0.00),
        (600050, 0.15),
        (None,   0.20),
    ],
    'married_separately': [
        (48350,  0.00),
        (300000, 0.15),
        (None,   0.20),
    ],
    'head_of_household': [
        (64750,  0.00),
        (566700, 0.15),
        (None,   0.20),
    ],
}

# FICA 2025
SS_WAGE_BASE = 176100
SS_RATE_EMPLOYEE = 0.062
MEDICARE_RATE_EMPLOYEE = 0.0145
ADDITIONAL_MEDICARE_RATE = 0.009
ADDITIONAL_MEDICARE_THRESHOLD = {
    'single':             200000,
    'married_jointly':    250000,
    'married_separately': 125000,
    'head_of_household':  200000,
}

# Self-employment tax
SE_DEDUCTION_FACTOR = 0.9235   # net profit × this = SE net earnings
SE_SS_RATE = 0.124             # 12.4% on net earnings up to SS_WAGE_BASE
SE_MEDICARE_RATE = 0.029       # 2.9% on all net earnings
SE_HALF_DEDUCTIBLE = 0.50      # deduct 50% of SE tax from income

# AMT 2025
AMT_EXEMPTION = {
    'single':             88100,
    'married_jointly':    137000,
    'married_separately': 68500,
    'head_of_household':  88100,
}
AMT_RATE_LOW  = 0.26
AMT_RATE_HIGH = 0.28
AMT_HIGH_THRESHOLD = 220700    # income above this: 28%

# Child Tax Credit
CHILD_TAX_CREDIT = 2000        # per qualifying child under 17
CTC_PHASEOUT_THRESHOLD = {
    'single':             200000,
    'married_jointly':    400000,
    'married_separately': 200000,
    'head_of_household':  200000,
}

# IRA / 401(k) limits 2025
IRA_LIMIT = 7000
IRA_CATCH_UP = 8000            # age 50+
K401_LIMIT = 23500
K401_CATCH_UP = 31000          # age 50+
HSA_LIMIT_SINGLE = 4300
HSA_LIMIT_FAMILY = 8550

FILING_STATUS_LABELS = {
    'single':             'Single',
    'married_jointly':    'Married Filing Jointly',
    'married_separately': 'Married Filing Separately',
    'head_of_household':  'Head of Household',
}

TAX_YEAR = 2025
