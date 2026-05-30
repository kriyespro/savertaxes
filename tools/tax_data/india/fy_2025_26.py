# FY 2025-26 (AY 2026-27) — Income Tax Data
# Source: Finance Act 2025, CBDT

# ── New Regime ──────────────────────────────────────────────────────────────
NEW_REGIME_SLABS = [
    (400_000,  0.00),
    (800_000,  0.05),
    (1_200_000, 0.10),
    (1_600_000, 0.15),
    (2_000_000, 0.20),
    (2_400_000, 0.25),
    (None,     0.30),
]
NEW_REGIME_STD_DEDUCTION = 75_000
NEW_REGIME_REBATE_LIMIT = 1_200_000   # income up to ₹12L → 0 tax
NEW_REGIME_REBATE_MAX = 60_000

# ── Old Regime ───────────────────────────────────────────────────────────────
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

# ── Cess & Surcharge ─────────────────────────────────────────────────────────
CESS_RATE = 0.04

SURCHARGE_SLABS = [
    (5_000_000,  0.10),    # > ₹50 lakh
    (10_000_000, 0.15),    # > ₹1 crore
    (20_000_000, 0.25),    # > ₹2 crore
    (50_000_000, 0.37),    # > ₹5 crore (old regime; new regime capped at 25%)
]

# ── Deduction Limits ─────────────────────────────────────────────────────────
SECTION_80C_LIMIT = 150_000
SECTION_80D = {
    'self_family_below_60': 25_000,
    'self_family_60_plus':  50_000,
    'parents_below_60':     25_000,
    'parents_60_plus':      50_000,
}
SECTION_80CCD_1B = 50_000       # NPS extra over 80C
SECTION_24B_LIMIT = 200_000     # Home loan interest (self-occupied)
SECTION_80EEA_LIMIT = 150_000   # Affordable housing extra
SECTION_80E_LIMIT = None        # No limit — education loan interest
SECTION_80G_RATES = [1.00, 0.50]
SECTION_80TTA_LIMIT = 10_000    # Savings interest (below 60)
SECTION_80TTB_LIMIT = 50_000    # FD interest for senior citizens

# ── Capital Gains (post Budget 2024) ─────────────────────────────────────────
STCG_EQUITY_RATE = 0.20          # < 12 months holding
LTCG_EQUITY_RATE = 0.125         # > 12 months, above ₹1.25L exemption
LTCG_EQUITY_EXEMPTION = 125_000
STCG_PROPERTY_RATE = None        # Slab rate (< 24 months)
LTCG_PROPERTY_RATE = 0.125       # > 24 months, no indexation
CRYPTO_TAX_RATE = 0.30
CRYPTO_TDS_RATE = 0.01

# ── Advance Tax Due Dates ─────────────────────────────────────────────────────
ADVANCE_TAX_SCHEDULE = [
    ('Jun 15', 0.15),
    ('Sep 15', 0.45),
    ('Dec 15', 0.75),
    ('Mar 15', 1.00),
]
ADVANCE_TAX_THRESHOLD = 10_000
