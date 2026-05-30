"""
US Federal Tax Calculation Engine — Tax Year 2025
All logic here. Nothing in views or templates.
"""
from .tax_data.us import federal_2025 as fed


def _apply_brackets(income, brackets):
    """Apply progressive tax brackets. Returns tax amount."""
    tax = 0
    prev = 0
    for limit, rate in brackets:
        if income <= prev:
            break
        taxable = (min(income, limit) if limit else income) - prev
        tax += taxable * rate
        if limit:
            prev = limit
    return round(tax, 2)


def _bracket_breakdown(income, brackets):
    """Return list of {rate, income_in_bracket, tax} for display."""
    breakdown = []
    prev = 0
    for limit, rate in brackets:
        if income <= prev:
            break
        cap = min(income, limit) if limit else income
        amount = cap - prev
        breakdown.append({
            'rate': rate,
            'rate_pct': f'{rate * 100:.0f}%',
            'income_in_bracket': round(amount),
            'tax': round(amount * rate, 2),
        })
        if limit:
            prev = limit
    return breakdown


def calculate_federal_tax(gross_income, filing_status='single',
                          use_standard_deduction=True, itemized_deductions=0,
                          num_children=0, other_credits=0):
    """
    Full federal income tax calculation.
    Returns dict with tax liability, effective rate, slab breakdown, credits.
    """
    gross_income = max(0, int(gross_income))
    filing_status = filing_status if filing_status in fed.BRACKETS else 'single'

    deduction = (fed.STANDARD_DEDUCTION[filing_status]
                 if use_standard_deduction
                 else max(itemized_deductions, 0))

    taxable_income = max(0, gross_income - deduction)
    brackets = fed.BRACKETS[filing_status]

    raw_tax = _apply_brackets(taxable_income, brackets)
    breakdown = _bracket_breakdown(taxable_income, brackets)

    # Child Tax Credit
    ctc_phaseout = fed.CTC_PHASEOUT_THRESHOLD[filing_status]
    ctc = num_children * fed.CHILD_TAX_CREDIT
    if gross_income > ctc_phaseout:
        phaseout_reduction = ((gross_income - ctc_phaseout) // 1000) * 50
        ctc = max(0, ctc - phaseout_reduction)

    total_credits = ctc + max(0, other_credits)
    tax_after_credits = max(0, raw_tax - total_credits)

    effective_rate = (tax_after_credits / gross_income * 100) if gross_income > 0 else 0
    marginal_rate = next(
        (rate for limit, rate in brackets if limit is None or taxable_income <= limit),
        0.37
    )

    return {
        'type': 'us_federal_tax',
        'gross_income': gross_income,
        'deduction': deduction,
        'deduction_type': 'Standard' if use_standard_deduction else 'Itemized',
        'taxable_income': taxable_income,
        'filing_status': filing_status,
        'filing_status_label': fed.FILING_STATUS_LABELS[filing_status],
        'raw_tax': round(raw_tax, 2),
        'ctc': round(ctc, 2),
        'other_credits': round(other_credits, 2),
        'total_credits': round(total_credits, 2),
        'federal_tax': round(tax_after_credits, 2),
        'effective_rate': round(effective_rate, 2),
        'marginal_rate': marginal_rate,
        'marginal_rate_pct': f'{marginal_rate * 100:.0f}%',
        'breakdown': breakdown,
        'take_home': gross_income - round(tax_after_credits, 2),
    }


def calculate_se_tax(net_profit, filing_status='single'):
    """
    Self-employment tax + income tax for 1099 / Schedule C filers.
    SE tax = 15.3% on 92.35% of net profit (up to SS wage base), then 2.9%.
    50% of SE tax is deductible from income tax.
    """
    net_profit = max(0, float(net_profit))

    se_earnings = net_profit * fed.SE_DEDUCTION_FACTOR

    # SS portion (capped at wage base)
    ss_earnings = min(se_earnings, fed.SS_WAGE_BASE)
    ss_tax = ss_earnings * fed.SE_SS_RATE

    # Medicare (uncapped)
    medicare_tax = se_earnings * fed.SE_MEDICARE_RATE

    se_tax = round(ss_tax + medicare_tax, 2)

    # Deduct 50% of SE tax from income for federal tax calc
    se_deduction = round(se_tax * fed.SE_HALF_DEDUCTIBLE, 2)
    adjusted_income = max(0, net_profit - se_deduction)

    fed_result = calculate_federal_tax(adjusted_income, filing_status)

    total_tax = round(se_tax + fed_result['federal_tax'], 2)
    effective_total_rate = round(total_tax / net_profit * 100, 2) if net_profit > 0 else 0

    quarterly = round(total_tax / 4, 2)

    return {
        'type': 'us_se_tax',
        'net_profit': round(net_profit),
        'se_earnings': round(se_earnings),
        'ss_tax': round(ss_tax, 2),
        'medicare_tax': round(medicare_tax, 2),
        'se_tax': se_tax,
        'se_deduction': se_deduction,
        'adjusted_income': round(adjusted_income),
        'federal_tax': fed_result['federal_tax'],
        'total_tax': total_tax,
        'effective_total_rate': effective_total_rate,
        'quarterly_payment': quarterly,
        'take_home': round(net_profit - total_tax),
        'breakdown': fed_result['breakdown'],
    }


def calculate_capital_gains(total_income, short_term_gain=0, long_term_gain=0,
                            filing_status='single'):
    """
    Capital gains tax calculator.
    Short-term: taxed as ordinary income.
    Long-term: 0% / 15% / 20% preferential rates + potential 3.8% NIIT.
    """
    total_income = max(0, float(total_income))
    short_term_gain = max(0, float(short_term_gain))
    long_term_gain = max(0, float(long_term_gain))
    filing_status = filing_status if filing_status in fed.BRACKETS else 'single'

    # Short-term: add to ordinary income, taxed at marginal rate
    ordinary_income = total_income + short_term_gain
    fed_result = calculate_federal_tax(ordinary_income, filing_status)
    st_tax = round(fed_result['federal_tax'] -
                   calculate_federal_tax(total_income, filing_status)['federal_tax'], 2)
    st_tax = max(0, st_tax)

    # Long-term: preferential brackets
    lt_brackets = fed.LTCG_BRACKETS[filing_status]
    lt_tax = round(_apply_brackets(long_term_gain, lt_brackets), 2)

    # NIIT (3.8%) — applies to net investment income if above threshold
    niit_threshold = fed.ADDITIONAL_MEDICARE_THRESHOLD[filing_status]
    niit_base = max(0, min(long_term_gain + short_term_gain,
                           ordinary_income + long_term_gain - niit_threshold))
    niit = round(niit_base * 0.038, 2) if ordinary_income + long_term_gain > niit_threshold else 0

    total_tax = st_tax + lt_tax + niit

    lt_rate = 0
    for limit, rate in lt_brackets:
        if limit is None or long_term_gain <= limit:
            lt_rate = rate
            break

    return {
        'type': 'us_capital_gains',
        'total_income': round(total_income),
        'short_term_gain': round(short_term_gain),
        'long_term_gain': round(long_term_gain),
        'st_tax': st_tax,
        'lt_tax': lt_tax,
        'lt_rate_pct': f'{lt_rate * 100:.0f}%',
        'niit': niit,
        'total_tax': round(total_tax, 2),
        'effective_rate': round(total_tax / (short_term_gain + long_term_gain) * 100, 2)
                          if (short_term_gain + long_term_gain) > 0 else 0,
        'filing_status_label': fed.FILING_STATUS_LABELS[filing_status],
    }


def calculate_tax_refund(gross_income, total_withholding, filing_status='single',
                         use_standard_deduction=True, itemized_deductions=0,
                         num_children=0, other_credits=0):
    """Estimate tax refund or amount owed."""
    fed_result = calculate_federal_tax(
        gross_income, filing_status, use_standard_deduction,
        itemized_deductions, num_children, other_credits
    )
    tax_owed = fed_result['federal_tax']
    total_withholding = max(0, float(total_withholding))

    net = total_withholding - tax_owed
    return {
        'type': 'us_refund',
        'gross_income': gross_income,
        'tax_owed': round(tax_owed, 2),
        'withholding': round(total_withholding, 2),
        'refund': round(net, 2) if net >= 0 else 0,
        'owe': round(abs(net), 2) if net < 0 else 0,
        'is_refund': net >= 0,
        'effective_rate': fed_result['effective_rate'],
        'filing_status_label': fed.FILING_STATUS_LABELS[filing_status],
    }


def calculate_quarterly_estimated_tax(annual_income, filing_status='single',
                                      is_self_employed=False, prior_year_tax=0):
    """
    Quarterly estimated tax due dates + safe harbor.
    Safe harbor: 100% of prior year tax (110% if income > $150K).
    """
    if is_self_employed:
        result = calculate_se_tax(annual_income, filing_status)
        annual_tax = result['total_tax']
    else:
        result = calculate_federal_tax(annual_income, filing_status)
        annual_tax = result['federal_tax']

    prior_year_tax = float(prior_year_tax)
    safe_harbor_rate = 1.10 if annual_income > 150000 else 1.00
    safe_harbor = round(prior_year_tax * safe_harbor_rate, 2) if prior_year_tax > 0 else None

    quarterly = round(annual_tax / 4, 2)

    return {
        'type': 'us_quarterly',
        'annual_tax': round(annual_tax, 2),
        'quarterly': quarterly,
        'q1_due': 'April 15, 2025',
        'q2_due': 'June 16, 2025',
        'q3_due': 'September 15, 2025',
        'q4_due': 'January 15, 2026',
        'q1': quarterly,
        'q2': quarterly,
        'q3': quarterly,
        'q4': quarterly,
        'safe_harbor': safe_harbor,
        'safe_harbor_quarterly': round(safe_harbor / 4, 2) if safe_harbor else None,
        'is_self_employed': is_self_employed,
    }


def calculate_standard_vs_itemized(filing_status='single', mortgage_interest=0,
                                   state_local_taxes=0, charitable=0,
                                   medical=0, gross_income=0, other=0):
    """Compare standard vs itemized deduction."""
    filing_status = filing_status if filing_status in fed.STANDARD_DEDUCTION else 'single'
    standard = fed.STANDARD_DEDUCTION[filing_status]

    salt_cap = 10000  # SALT cap ($10K) under TCJA (expires end of 2025)
    capped_salt = min(float(state_local_taxes), salt_cap)

    gross_income = max(0, float(gross_income))
    # Medical deduction: only amount exceeding 7.5% of AGI
    medical_threshold = gross_income * 0.075
    deductible_medical = max(0, float(medical) - medical_threshold)

    itemized = (float(mortgage_interest) + capped_salt +
                float(charitable) + deductible_medical + float(other))
    itemized = round(itemized, 2)

    winner = 'standard' if standard >= itemized else 'itemized'
    savings = abs(standard - itemized)

    # Tax savings of choosing winner
    if gross_income > 0:
        tax_with_standard = calculate_federal_tax(gross_income, filing_status, True)['federal_tax']
        tax_with_itemized = calculate_federal_tax(gross_income, filing_status, False, itemized)['federal_tax']
        tax_difference = round(abs(tax_with_standard - tax_with_itemized), 2)
    else:
        tax_difference = 0

    return {
        'type': 'us_std_vs_itemized',
        'standard': standard,
        'itemized': round(itemized),
        'winner': winner,
        'deduction_difference': round(savings),
        'tax_difference': tax_difference,
        'salt_capped': float(state_local_taxes) > salt_cap,
        'capped_salt': round(capped_salt),
        'deductible_medical': round(deductible_medical),
        'filing_status_label': fed.FILING_STATUS_LABELS[filing_status],
    }


def calculate_paycheck(annual_salary, filing_status='single',
                       pay_frequency='biweekly', state_tax_rate=0,
                       pre_tax_401k=0, pre_tax_hsa=0, pre_tax_medical=0):
    """
    Paycheck take-home calculator.
    Handles federal tax, SS, Medicare, state tax (flat rate), pre-tax deductions.
    """
    annual_salary = max(0, float(annual_salary))
    filing_status = filing_status if filing_status in fed.BRACKETS else 'single'

    freq_map = {'weekly': 52, 'biweekly': 26, 'semimonthly': 24, 'monthly': 12}
    periods = freq_map.get(pay_frequency, 26)

    # Pre-tax deductions reduce federal taxable income
    pre_tax_total = float(pre_tax_401k) + float(pre_tax_hsa) + float(pre_tax_medical)
    taxable_salary = max(0, annual_salary - pre_tax_total)

    fed_result = calculate_federal_tax(taxable_salary, filing_status)
    annual_federal = fed_result['federal_tax']

    # FICA on actual salary (SS) and taxable salary (Medicare)
    ss_wages = min(annual_salary, fed.SS_WAGE_BASE)
    annual_ss = round(ss_wages * fed.SS_RATE_EMPLOYEE, 2)
    annual_medicare = round(annual_salary * fed.MEDICARE_RATE_EMPLOYEE, 2)

    # Additional Medicare
    threshold = fed.ADDITIONAL_MEDICARE_THRESHOLD[filing_status]
    if annual_salary > threshold:
        annual_medicare += round((annual_salary - threshold) * fed.ADDITIONAL_MEDICARE_RATE, 2)

    # State tax
    annual_state = round(annual_salary * float(state_tax_rate) / 100, 2)

    annual_take_home = (annual_salary - annual_federal - annual_ss -
                        annual_medicare - annual_state - pre_tax_total)

    per_period = lambda x: round(x / periods, 2)

    return {
        'type': 'us_paycheck',
        'annual_salary': round(annual_salary),
        'pay_frequency': pay_frequency,
        'periods_per_year': periods,
        'gross_per_period': per_period(annual_salary),
        'pre_tax_deductions': round(pre_tax_total, 2),
        'federal_tax_annual': round(annual_federal, 2),
        'federal_tax_per_period': per_period(annual_federal),
        'ss_annual': annual_ss,
        'ss_per_period': per_period(annual_ss),
        'medicare_annual': annual_medicare,
        'medicare_per_period': per_period(annual_medicare),
        'state_tax_annual': annual_state,
        'state_tax_per_period': per_period(annual_state),
        'pre_tax_per_period': per_period(pre_tax_total),
        'net_take_home_annual': round(annual_take_home, 2),
        'net_take_home_per_period': per_period(annual_take_home),
        'effective_rate': round((annual_federal + annual_ss + annual_medicare) /
                                annual_salary * 100, 2) if annual_salary > 0 else 0,
        'filing_status_label': fed.FILING_STATUS_LABELS[filing_status],
    }
