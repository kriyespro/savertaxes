# FY 2024-25 (AY 2025-26) — Income Tax Data

NEW_REGIME_SLABS = [
    (300_000,   0.00),
    (600_000,   0.05),
    (900_000,   0.10),
    (1_200_000, 0.15),
    (1_500_000, 0.20),
    (None,      0.30),
]
NEW_REGIME_STD_DEDUCTION = 75_000
NEW_REGIME_REBATE_LIMIT = 700_000
NEW_REGIME_REBATE_MAX = 25_000

OLD_REGIME_SLABS = {
    'below_60': [
        (250_000, 0.00),
        (500_000, 0.05),
        (1_000_000, 0.20),
        (None, 0.30),
    ],
    '60_to_79': [
        (300_000, 0.00),
        (500_000, 0.05),
        (1_000_000, 0.20),
        (None, 0.30),
    ],
    '80_plus': [
        (500_000, 0.00),
        (1_000_000, 0.20),
        (None, 0.30),
    ],
}
OLD_REGIME_STD_DEDUCTION = 50_000
OLD_REGIME_REBATE_LIMIT = 500_000
OLD_REGIME_REBATE_MAX = 12_500

CESS_RATE = 0.04

SURCHARGE_SLABS = [
    (5_000_000,  0.10),
    (10_000_000, 0.15),
    (20_000_000, 0.25),
    (50_000_000, 0.37),
]

SECTION_80C_LIMIT = 150_000
SECTION_80D = {
    'self_family_below_60': 25_000,
    'self_family_60_plus':  50_000,
    'parents_below_60':     25_000,
    'parents_60_plus':      50_000,
}
SECTION_80CCD_1B = 50_000
SECTION_24B_LIMIT = 200_000
SECTION_80EEA_LIMIT = 150_000
SECTION_80E_LIMIT = None
SECTION_80G_RATES = [1.00, 0.50]
SECTION_80TTA_LIMIT = 10_000
SECTION_80TTB_LIMIT = 50_000

# Pre-Budget 2024 rates (Budget 2024 changed to 20%/12.5% from July 23, 2024)
STCG_EQUITY_RATE = 0.15
LTCG_EQUITY_RATE = 0.10
LTCG_EQUITY_EXEMPTION = 100_000
STCG_PROPERTY_RATE = None
LTCG_PROPERTY_RATE = 0.20    # Pre-Budget 2024 (with indexation)

ADVANCE_TAX_SCHEDULE = [
    ('Jun 15', 0.15),
    ('Sep 15', 0.45),
    ('Dec 15', 0.75),
    ('Mar 15', 1.00),
]
ADVANCE_TAX_THRESHOLD = 10_000
