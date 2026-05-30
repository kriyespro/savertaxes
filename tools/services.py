"""
Tax calculation engine — ALL logic lives here.
No tax math in views or templates.
"""
from tools.tax_data.india import fy_2025_26 as fy26
from tools.tax_data.india import fy_2024_25 as fy25


def _get_fy_data(fy='2025-26'):
    return fy26 if fy == '2025-26' else fy25


# ── Core slab engine ─────────────────────────────────────────────────────────

def _apply_slabs(income, slabs):
    tax = 0
    prev = 0
    breakdown = []
    for limit, rate in slabs:
        if income <= prev:
            break
        upper = limit if limit is not None else income
        taxable = min(income, upper) - prev
        slab_tax = taxable * rate
        if taxable > 0:
            breakdown.append({
                'from': prev, 'to': upper if limit else income,
                'rate': rate * 100, 'taxable': taxable, 'tax': slab_tax
            })
        tax += slab_tax
        prev = upper
        if limit is None:
            break
    return tax, breakdown


def _apply_surcharge(income, tax, data):
    surcharge_rate = 0
    for limit, rate in data.SURCHARGE_SLABS:
        if income > limit:
            surcharge_rate = rate
    surcharge = tax * surcharge_rate
    # Marginal relief: ensure surcharge doesn't exceed income above threshold
    return surcharge, surcharge_rate


def _apply_rebate(income, tax, limit, max_rebate):
    if income <= limit:
        return min(tax, max_rebate)
    return 0


def _final_tax(tax_before_cess, data):
    cess = tax_before_cess * data.CESS_RATE
    return tax_before_cess + cess


# ── New Regime ───────────────────────────────────────────────────────────────

def calculate_new_regime(gross_income, fy='2025-26'):
    data = _get_fy_data(fy)
    taxable = max(0, gross_income - data.NEW_REGIME_STD_DEDUCTION)
    raw_tax, breakdown = _apply_slabs(taxable, data.NEW_REGIME_SLABS)
    rebate = _apply_rebate(taxable, raw_tax, data.NEW_REGIME_REBATE_LIMIT, data.NEW_REGIME_REBATE_MAX)
    tax_after_rebate = max(0, raw_tax - rebate)
    surcharge, surcharge_rate = _apply_surcharge(taxable, tax_after_rebate, data)
    tax_with_surcharge = tax_after_rebate + surcharge
    cess = tax_with_surcharge * data.CESS_RATE
    total_tax = tax_with_surcharge + cess
    effective_rate = (total_tax / gross_income * 100) if gross_income else 0
    marginal_rate = breakdown[-1]['rate'] if breakdown else 0
    return {
        'regime': 'new',
        'gross_income': gross_income,
        'std_deduction': data.NEW_REGIME_STD_DEDUCTION,
        'taxable_income': taxable,
        'slab_tax': raw_tax,
        'rebate_87a': rebate,
        'surcharge': surcharge,
        'surcharge_rate': surcharge_rate * 100,
        'cess': cess,
        'total_tax': round(total_tax),
        'take_home_yearly': round(gross_income - total_tax),
        'take_home_monthly': round((gross_income - total_tax) / 12),
        'effective_rate': round(effective_rate, 2),
        'marginal_rate': marginal_rate,
        'breakdown': breakdown,
    }


# ── Old Regime ───────────────────────────────────────────────────────────────

def calculate_old_regime(gross_income, age_group='below_60', deductions=None, fy='2025-26'):
    data = _get_fy_data(fy)
    d = deductions or {}

    std_ded = data.OLD_REGIME_STD_DEDUCTION
    sec_80c = min(d.get('sec_80c', 0), data.SECTION_80C_LIMIT)
    sec_80d_self = min(d.get('sec_80d_self', 0), data.SECTION_80D['self_family_below_60'])
    sec_80d_parents = min(d.get('sec_80d_parents', 0), data.SECTION_80D['parents_60_plus'])
    hra = d.get('hra_exemption', 0)
    home_loan_interest = min(d.get('home_loan_interest', 0), data.SECTION_24B_LIMIT)
    nps_80ccd = min(d.get('nps_extra', 0), data.SECTION_80CCD_1B)
    other_deductions = d.get('other', 0)

    total_deductions = (std_ded + sec_80c + sec_80d_self + sec_80d_parents +
                        hra + home_loan_interest + nps_80ccd + other_deductions)

    taxable = max(0, gross_income - total_deductions)
    slabs = data.OLD_REGIME_SLABS.get(age_group, data.OLD_REGIME_SLABS['below_60'])
    raw_tax, breakdown = _apply_slabs(taxable, slabs)

    rebate = _apply_rebate(taxable, raw_tax, data.OLD_REGIME_REBATE_LIMIT, data.OLD_REGIME_REBATE_MAX)
    tax_after_rebate = max(0, raw_tax - rebate)
    surcharge, surcharge_rate = _apply_surcharge(taxable, tax_after_rebate, data)
    tax_with_surcharge = tax_after_rebate + surcharge
    cess = tax_with_surcharge * data.CESS_RATE
    total_tax = tax_with_surcharge + cess

    effective_rate = (total_tax / gross_income * 100) if gross_income else 0
    marginal_rate = breakdown[-1]['rate'] if breakdown else 0

    return {
        'regime': 'old',
        'gross_income': gross_income,
        'std_deduction': std_ded,
        'sec_80c': sec_80c,
        'sec_80d': sec_80d_self + sec_80d_parents,
        'hra_exemption': hra,
        'home_loan_interest': home_loan_interest,
        'nps_extra': nps_80ccd,
        'total_deductions': round(total_deductions),
        'taxable_income': round(taxable),
        'slab_tax': round(raw_tax),
        'rebate_87a': round(rebate),
        'surcharge': round(surcharge),
        'surcharge_rate': surcharge_rate * 100,
        'cess': round(cess),
        'total_tax': round(total_tax),
        'take_home_yearly': round(gross_income - total_tax),
        'take_home_monthly': round((gross_income - total_tax) / 12),
        'effective_rate': round(effective_rate, 2),
        'marginal_rate': marginal_rate,
        'breakdown': breakdown,
    }


# ── Regime Comparison (T01 — most important tool) ────────────────────────────

def compare_regimes(gross_income, age_group='below_60', deductions=None, fy='2025-26'):
    new = calculate_new_regime(gross_income, fy)
    old = calculate_old_regime(gross_income, age_group, deductions, fy)
    saving = old['total_tax'] - new['total_tax']
    winner = 'new' if new['total_tax'] <= old['total_tax'] else 'old'
    return {
        'new': new,
        'old': old,
        'winner': winner,
        'savings': abs(saving),
        'savings_monthly': abs(round(saving / 12)),
        'winner_label': 'New Regime' if winner == 'new' else 'Old Regime',
    }


# ── HRA Exemption (T04) ───────────────────────────────────────────────────────

def calculate_hra_exemption(basic_salary, hra_received, annual_rent, is_metro):
    metro_pct = 0.50 if is_metro else 0.40
    option1 = hra_received
    option2 = basic_salary * metro_pct
    option3 = max(0, annual_rent - 0.10 * basic_salary)
    exemption = min(option1, option2, option3)
    taxable_hra = hra_received - exemption
    return {
        'hra_received': hra_received,
        'exemption': round(exemption),
        'taxable_hra': round(taxable_hra),
        'option1_hra_received': round(option1),
        'option2_pct_of_basic': round(option2),
        'option3_rent_minus_10pct': round(option3),
        'is_metro': is_metro,
    }


# ── Advance Tax (T05) ─────────────────────────────────────────────────────────

def calculate_advance_tax(annual_tax_liability, tds_deducted=0, fy='2025-26'):
    data = _get_fy_data(fy)
    net_liability = max(0, annual_tax_liability - tds_deducted)
    if net_liability <= data.ADVANCE_TAX_THRESHOLD:
        return {'required': False, 'threshold': data.ADVANCE_TAX_THRESHOLD}
    schedule = []
    for date_label, pct in data.ADVANCE_TAX_SCHEDULE:
        installment = round(net_liability * pct)
        schedule.append({'date': date_label, 'cumulative_pct': pct * 100,
                         'cumulative_amount': installment,
                         'installment': round(net_liability * pct -
                                              (schedule[-1]['cumulative_amount'] if schedule else 0))})
    return {
        'required': True,
        'annual_tax': annual_tax_liability,
        'tds_deducted': tds_deducted,
        'net_liability': net_liability,
        'schedule': schedule,
    }


# ── Capital Gains — Equity / MF (T10) ────────────────────────────────────────

def calculate_capital_gains_equity(buy_price, sell_price, units, holding_months, fy='2025-26'):
    data = _get_fy_data(fy)
    gain = (sell_price - buy_price) * units
    if holding_months < 12:
        gain_type = 'STCG'
        tax_rate = data.STCG_EQUITY_RATE
        tax = max(0, gain) * tax_rate
        exemption = 0
    else:
        gain_type = 'LTCG'
        tax_rate = data.LTCG_EQUITY_RATE
        exemption = data.LTCG_EQUITY_EXEMPTION
        taxable_gain = max(0, gain - exemption)
        tax = taxable_gain * tax_rate
    cess = tax * data.CESS_RATE
    total_tax = tax + cess
    return {
        'gain_type': gain_type,
        'total_gain': round(gain),
        'exemption': round(exemption),
        'taxable_gain': round(max(0, gain - exemption)),
        'tax_rate': tax_rate * 100,
        'tax_before_cess': round(tax),
        'cess': round(cess),
        'total_tax': round(total_tax),
        'net_profit': round(gain - total_tax),
    }


# ── GST Calculator (T09) ─────────────────────────────────────────────────────

def calculate_gst(amount, rate_pct, reverse=False):
    rate = rate_pct / 100
    if reverse:
        original = amount / (1 + rate)
        gst_amount = amount - original
        return {
            'original_amount': round(original, 2),
            'gst_amount': round(gst_amount, 2),
            'total_amount': round(amount, 2),
            'cgst': round(gst_amount / 2, 2),
            'sgst': round(gst_amount / 2, 2),
            'rate_pct': rate_pct,
            'reverse': True,
        }
    gst_amount = amount * rate
    total = amount + gst_amount
    return {
        'original_amount': round(amount, 2),
        'gst_amount': round(gst_amount, 2),
        'total_amount': round(total, 2),
        'cgst': round(gst_amount / 2, 2),
        'sgst': round(gst_amount / 2, 2),
        'rate_pct': rate_pct,
        'reverse': False,
    }


# ── Presumptive Tax 44ADA (T12) ───────────────────────────────────────────────

def calculate_presumptive_44ada(gross_receipts, fy='2025-26'):
    presumptive_income = gross_receipts * 0.50
    new = calculate_new_regime(presumptive_income, fy)
    old = calculate_old_regime(presumptive_income, fy=fy)
    return {
        'gross_receipts': gross_receipts,
        'presumptive_income': round(presumptive_income),
        'new_regime': new,
        'old_regime': old,
        'winner': 'new' if new['total_tax'] <= old['total_tax'] else 'old',
    }


# ── Section 80C Planner (T06) ─────────────────────────────────────────────────

def calculate_80c_savings(gross_income, current_80c_investment, marginal_rate_pct, fy='2025-26'):
    data = _get_fy_data(fy)
    remaining = max(0, data.SECTION_80C_LIMIT - current_80c_investment)
    tax_saving = remaining * (marginal_rate_pct / 100) * (1 + data.CESS_RATE)
    return {
        'limit': data.SECTION_80C_LIMIT,
        'invested': current_80c_investment,
        'remaining': remaining,
        'potential_tax_saving': round(tax_saving),
    }


# ── CTC to Take-Home (T03) ────────────────────────────────────────────────────

def calculate_ctc_to_takehome(ctc, basic_pct=40.0, hra_pct=50.0, regime='new',
                               age_group='below_60', fy='2025-26'):
    basic_annual = ctc * basic_pct / 100
    hra_annual = basic_annual * hra_pct / 100
    employer_pf = basic_annual * 0.12
    gratuity = basic_annual * 0.0481
    gross_salary = max(0, ctc - employer_pf - gratuity)

    if regime == 'new':
        tax_result = calculate_new_regime(gross_salary, fy)
    else:
        tax_result = calculate_old_regime(gross_salary, age_group, fy=fy)

    annual_tds = tax_result['total_tax']
    employee_pf = basic_annual * 0.12
    prof_tax_annual = 2_400
    special_allowance = max(0, gross_salary - basic_annual - hra_annual)

    deductions_annual = employee_pf + annual_tds + prof_tax_annual
    take_home_annual = gross_salary - deductions_annual

    return {
        'ctc': ctc,
        'gross_salary': round(gross_salary),
        'basic_monthly': round(basic_annual / 12),
        'hra_monthly': round(hra_annual / 12),
        'special_allowance_monthly': round(special_allowance / 12),
        'employer_pf_annual': round(employer_pf),
        'gratuity_annual': round(gratuity),
        'employee_pf_monthly': round(employee_pf / 12),
        'tds_monthly': round(annual_tds / 12),
        'tds_annual': round(annual_tds),
        'prof_tax_monthly': round(prof_tax_annual / 12),
        'take_home_monthly': round(take_home_annual / 12),
        'take_home_annual': round(take_home_annual),
        'effective_rate': tax_result['effective_rate'],
        'regime': regime,
    }


# ── Section 80D Calculator (T07) ─────────────────────────────────────────────

def calculate_80d_savings(premium_self, senior_self, premium_parents, senior_parents,
                          preventive_self=0, preventive_parents=0,
                          marginal_rate_pct=30.0, fy='2025-26'):
    data = _get_fy_data(fy)
    self_limit = (data.SECTION_80D['self_family_60_plus'] if senior_self
                  else data.SECTION_80D['self_family_below_60'])
    parents_limit = (data.SECTION_80D['parents_60_plus'] if senior_parents
                     else data.SECTION_80D['parents_below_60'])

    self_deduction = min(premium_self + preventive_self, self_limit)
    parents_deduction = min(premium_parents + preventive_parents, parents_limit)
    total_deduction = self_deduction + parents_deduction
    tax_saved = total_deduction * (marginal_rate_pct / 100) * (1 + data.CESS_RATE)

    return {
        'self_premium': premium_self,
        'parents_premium': premium_parents,
        'self_deduction': round(self_deduction),
        'parents_deduction': round(parents_deduction),
        'self_limit': self_limit,
        'parents_limit': parents_limit,
        'total_deduction': round(total_deduction),
        'tax_saved': round(tax_saved),
        'marginal_rate_pct': marginal_rate_pct,
    }


# ── TDS on Salary Calculator (T08) ───────────────────────────────────────────

def calculate_tds_on_salary(gross_income, regime='new', age_group='below_60',
                             deductions=None, fy='2025-26'):
    if regime == 'new':
        tax_result = calculate_new_regime(gross_income, fy)
    else:
        tax_result = calculate_old_regime(gross_income, age_group, deductions or {}, fy)

    annual_tax = tax_result['total_tax']
    return {
        'gross_income': gross_income,
        'annual_tax': annual_tax,
        'monthly_tds': round(annual_tax / 12),
        'regime': regime,
        'effective_rate': tax_result['effective_rate'],
        'take_home_monthly': tax_result['take_home_monthly'],
        'tds_result': tax_result,
    }


# ── Income Tax Refund Estimator (T11) ────────────────────────────────────────

def calculate_refund_or_demand(gross_income, tds_deducted, advance_tax_paid=0,
                                regime='new', age_group='below_60',
                                deductions=None, fy='2025-26'):
    if regime == 'new':
        tax_result = calculate_new_regime(gross_income, fy)
    else:
        tax_result = calculate_old_regime(gross_income, age_group, deductions or {}, fy)

    total_tax = tax_result['total_tax']
    total_paid = tds_deducted + advance_tax_paid
    excess = total_paid - total_tax

    return {
        'gross_income': gross_income,
        'total_tax': total_tax,
        'tds_deducted': tds_deducted,
        'advance_tax_paid': advance_tax_paid,
        'total_paid': total_paid,
        'refund': max(0, excess),
        'demand': max(0, -excess),
        'is_refund': excess > 0,
        'regime': regime,
        'effective_rate': tax_result['effective_rate'],
    }


# ── Home Loan Tax Benefit (T13) ───────────────────────────────────────────────

def calculate_home_loan_benefit(loan_amount, interest_rate_pct, loan_tenure_years,
                                 loan_year=1, is_self_occupied=True,
                                 marginal_rate_pct=30.0, fy='2025-26'):
    data = _get_fy_data(fy)
    r = interest_rate_pct / 100 / 12
    n = loan_tenure_years * 12

    if r > 0 and n > 0:
        emi = loan_amount * r * (1 + r) ** n / ((1 + r) ** n - 1)
    else:
        emi = loan_amount / max(n, 1)

    balance = loan_amount
    month_start = (loan_year - 1) * 12
    for _ in range(month_start):
        interest = balance * r
        balance -= (emi - interest)

    annual_interest = 0.0
    annual_principal = 0.0
    for _ in range(12):
        if balance <= 0:
            break
        interest = balance * r
        principal = min(emi - interest, balance)
        annual_interest += interest
        annual_principal += principal
        balance -= principal

    sec24 = min(annual_interest, data.SECTION_24B_LIMIT) if is_self_occupied else annual_interest
    sec80c_principal = min(annual_principal, data.SECTION_80C_LIMIT)
    total_deduction = sec24 + sec80c_principal
    tax_saved = total_deduction * (marginal_rate_pct / 100) * (1 + data.CESS_RATE)

    return {
        'loan_amount': loan_amount,
        'emi_monthly': round(emi),
        'annual_emi': round(emi * 12),
        'annual_interest': round(annual_interest),
        'annual_principal': round(annual_principal),
        'sec24_deduction': round(sec24),
        'sec80c_deduction': round(sec80c_principal),
        'total_deduction': round(total_deduction),
        'tax_saved': round(tax_saved),
        'is_self_occupied': is_self_occupied,
        'loan_year': loan_year,
        'section_24b_limit': data.SECTION_24B_LIMIT,
    }


# ── NPS Tax Benefit Calculator (T14) ─────────────────────────────────────────

def calculate_nps_benefit(basic_salary, employee_nps=0, employer_nps_pct=0.0,
                           other_80c=0, marginal_rate_pct=30.0, fy='2025-26'):
    data = _get_fy_data(fy)

    ccd1_max = basic_salary * 0.10
    ccd1_employee = min(employee_nps, ccd1_max)
    ccd1b = min(employee_nps, data.SECTION_80CCD_1B)

    employer_nps = basic_salary * employer_nps_pct / 100
    ccd2_max = basic_salary * 0.10
    ccd2 = min(employer_nps, ccd2_max)

    total_80c_used = min(ccd1_employee + other_80c, data.SECTION_80C_LIMIT)
    total_nps_extra = ccd1b + ccd2
    total_deduction = total_80c_used + total_nps_extra
    tax_saved = total_nps_extra * (marginal_rate_pct / 100) * (1 + data.CESS_RATE)

    return {
        'basic_salary': basic_salary,
        'employee_nps': employee_nps,
        'employer_nps': round(employer_nps),
        'ccd1_within_80c': round(ccd1_employee),
        'ccd1b_extra': round(ccd1b),
        'ccd2_employer': round(ccd2),
        'total_nps_extra_deduction': round(total_nps_extra),
        'total_deduction': round(total_deduction),
        'tax_saved': round(tax_saved),
        'marginal_rate_pct': marginal_rate_pct,
    }


# ── ITR Form Selector (T15) ───────────────────────────────────────────────────

def suggest_itr_form(has_salary, has_capital_gains, has_business_income,
                     has_presumptive, has_foreign_assets, is_director,
                     total_income, has_multiple_houses=False, has_fno=False):
    reasons = []

    if has_fno:
        reasons.append('F&O trading income is always treated as business income')
        return {'form': 'ITR-3', 'reasons': reasons, 'color': 'orange',
                'description': 'Business income (F&O)'}

    if has_business_income and not has_presumptive:
        reasons.append('Business income with actual books of accounts')
        if has_capital_gains:
            reasons.append('Capital gains are also reported in ITR-3')
        return {'form': 'ITR-3', 'reasons': reasons, 'color': 'orange',
                'description': 'Business/Profession with books'}

    if has_presumptive:
        if total_income > 5_000_000 or has_foreign_assets or is_director:
            reasons.append('Presumptive income, but total income exceeds ₹50L or foreign assets or director')
            return {'form': 'ITR-3', 'reasons': reasons, 'color': 'orange',
                    'description': 'Presumptive + disqualifying condition'}
        reasons.append('Presumptive income under 44ADA (professionals) or 44AD (business)')
        reasons.append('Simple form — no need to maintain books of accounts')
        return {'form': 'ITR-4', 'reasons': reasons, 'color': 'blue',
                'description': 'Presumptive taxation (44ADA / 44AD)'}

    if (has_capital_gains or has_foreign_assets or is_director
            or has_multiple_houses or total_income > 5_000_000):
        if has_capital_gains:
            reasons.append('Capital gains income (stocks, mutual funds, property)')
        if has_foreign_assets:
            reasons.append('Foreign assets or foreign income')
        if is_director:
            reasons.append('Director in a company (without business income)')
        if has_multiple_houses:
            reasons.append('More than one house property')
        if total_income > 5_000_000:
            reasons.append('Total income above ₹50 lakh')
        return {'form': 'ITR-2', 'reasons': reasons, 'color': 'purple',
                'description': 'Salary + Capital Gains / Multiple income sources'}

    reasons.append('Salary / pension income only')
    reasons.append('Income from one house property (or none)')
    reasons.append('Total income below ₹50 lakh')
    return {'form': 'ITR-1', 'reasons': reasons, 'color': 'green',
            'description': 'Sahaj — Simplest form for salaried individuals'}


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2 TOOLS (T16–T35)
# ═══════════════════════════════════════════════════════════════════════════════

# ── T16 — Section 80G Charitable Donation ────────────────────────────────────

def calculate_80g_deduction(donation_100pct, donation_50pct, marginal_rate_pct=30.0, fy='2025-26'):
    data = _get_fy_data(fy)
    deduction = donation_100pct + (donation_50pct * 0.50)
    tax_saved = deduction * (marginal_rate_pct / 100) * (1 + data.CESS_RATE)
    return {
        'donation_100pct': donation_100pct,
        'donation_50pct': donation_50pct,
        'deduction_100pct': donation_100pct,
        'deduction_50pct': round(donation_50pct * 0.50),
        'total_deduction': round(deduction),
        'tax_saved': round(tax_saved),
        'marginal_rate_pct': marginal_rate_pct,
    }


# ── T17 — 80TTA / 80TTB Savings Interest ────────────────────────────────────

def calculate_80tta_ttb(savings_interest, fd_interest, is_senior_citizen=False,
                         marginal_rate_pct=30.0, fy='2025-26'):
    data = _get_fy_data(fy)
    if is_senior_citizen:
        # 80TTB: up to ₹50,000 on all interest (savings + FD)
        total_interest = savings_interest + fd_interest
        limit = data.SECTION_80TTB_LIMIT
        deduction = min(total_interest, limit)
        section = '80TTB'
    else:
        # 80TTA: up to ₹10,000 on savings account interest only
        limit = data.SECTION_80TTA_LIMIT
        deduction = min(savings_interest, limit)
        section = '80TTA'
    tax_saved = deduction * (marginal_rate_pct / 100) * (1 + data.CESS_RATE)
    return {
        'savings_interest': savings_interest,
        'fd_interest': fd_interest,
        'is_senior_citizen': is_senior_citizen,
        'section': section,
        'limit': limit,
        'total_interest': savings_interest + fd_interest,
        'deduction': round(deduction),
        'tax_saved': round(tax_saved),
        'taxable_interest': round(savings_interest + fd_interest - deduction),
    }


# ── T18 — Section 44AD Presumptive Tax (Business) ────────────────────────────

def calculate_presumptive_44ad(gross_turnover, is_digital=False, fy='2025-26'):
    # Digital transactions: 6% of turnover; cash: 8%
    pct = 0.06 if is_digital else 0.08
    presumptive_income = gross_turnover * pct
    new = calculate_new_regime(presumptive_income, fy)
    old = calculate_old_regime(presumptive_income, fy=fy)
    return {
        'gross_turnover': gross_turnover,
        'presumptive_pct': pct * 100,
        'presumptive_income': round(presumptive_income),
        'new_regime': new,
        'old_regime': old,
        'winner': 'new' if new['total_tax'] <= old['total_tax'] else 'old',
        'limit': 3_00_00_000,
    }


# ── T19 — Freelancer Tax Planner ──────────────────────────────────────────────

def calculate_freelancer_plan(gross_receipts, regime='new', sec_80c=0,
                               sec_80d=0, nps_extra=0, fy='2025-26'):
    data = _get_fy_data(fy)
    presumptive_income = gross_receipts * 0.50
    if regime == 'new':
        tax_result = calculate_new_regime(presumptive_income, fy)
    else:
        deductions = {'sec_80c': sec_80c, 'sec_80d_self': sec_80d, 'nps_extra': nps_extra}
        tax_result = calculate_old_regime(presumptive_income, deductions=deductions, fy=fy)

    advance_tax = calculate_advance_tax(tax_result['total_tax'], fy=fy)
    itr = suggest_itr_form(False, False, False, True, False, False, presumptive_income)

    return {
        'gross_receipts': gross_receipts,
        'presumptive_income': round(presumptive_income),
        'total_tax': tax_result['total_tax'],
        'effective_rate': tax_result['effective_rate'],
        'advance_tax': advance_tax,
        'itr_form': itr['form'],
        'regime': regime,
        'quarterly_tax': round(tax_result['total_tax'] / 4) if tax_result['total_tax'] > data.ADVANCE_TAX_THRESHOLD else 0,
    }


# ── T21 — Capital Gains — Real Estate / Property ─────────────────────────────

def calculate_capital_gains_property(buy_price, sell_price, holding_months, fy='2025-26'):
    data = _get_fy_data(fy)
    gain = sell_price - buy_price
    if holding_months < 24:
        gain_type = 'STCG'
        # Taxed at slab rate — return effective rate from income tax
        tax_rate = None  # slab rate
        tax = 0  # user must add to income
        note = 'STCG on property taxed at your income slab rate. Add this gain to your income.'
    else:
        gain_type = 'LTCG'
        tax_rate = data.LTCG_PROPERTY_RATE
        tax = max(0, gain) * tax_rate
        cess = tax * data.CESS_RATE
        tax = tax + cess
        note = 'LTCG @12.5% (no indexation benefit from FY 2024-25 onwards — Budget 2024).'
    return {
        'buy_price': buy_price,
        'sell_price': sell_price,
        'total_gain': round(gain),
        'gain_type': gain_type,
        'holding_months': holding_months,
        'tax_rate': (tax_rate * 100) if tax_rate else 'Slab rate',
        'total_tax': round(tax),
        'net_profit': round(gain - tax),
        'note': note,
    }


# ── T22 — Mutual Fund Tax Calculator ─────────────────────────────────────────

def calculate_mutual_fund_tax(invested, current_value, holding_months,
                               fund_type='equity', fy='2025-26'):
    data = _get_fy_data(fy)
    gain = current_value - invested
    gain_type = 'STCG' if holding_months < 12 else 'LTCG'

    if fund_type == 'equity':
        if gain_type == 'STCG':
            rate = data.STCG_EQUITY_RATE
            exemption = 0
        else:
            rate = data.LTCG_EQUITY_RATE
            exemption = data.LTCG_EQUITY_EXEMPTION
    else:
        # Debt funds: slab rate (return advisory)
        return {
            'invested': invested,
            'current_value': current_value,
            'total_gain': round(gain),
            'fund_type': fund_type,
            'gain_type': 'Ordinary Income',
            'tax_rate': 'Slab rate',
            'total_tax': 0,
            'exemption': 0,
            'note': 'Debt fund gains are taxed as ordinary income at your slab rate (no LTCG benefit from FY 2023-24).',
            'is_debt': True,
        }

    taxable = max(0, gain - exemption)
    tax = taxable * rate
    cess = tax * data.CESS_RATE
    total_tax = tax + cess
    return {
        'invested': invested,
        'current_value': current_value,
        'total_gain': round(gain),
        'exemption': exemption,
        'taxable_gain': round(taxable),
        'fund_type': fund_type,
        'gain_type': gain_type,
        'tax_rate': rate * 100,
        'total_tax': round(total_tax),
        'net_profit': round(gain - total_tax),
        'is_debt': False,
    }


# ── T23 — ELSS vs PPF vs NPS Comparison ──────────────────────────────────────

def compare_elss_ppf_nps(annual_investment=50000, years=15, marginal_rate_pct=30.0, fy='2025-26'):
    data = _get_fy_data(fy)

    # ELSS: 3-yr lock-in, ~12% returns, LTCG tax on gains above ₹1.25L
    elss_rate = 0.12
    elss_maturity = annual_investment * ((1 + elss_rate) ** years - 1) / elss_rate
    elss_gain = elss_maturity - annual_investment * years
    elss_tax = max(0, elss_gain - data.LTCG_EQUITY_EXEMPTION) * data.LTCG_EQUITY_RATE * (1 + data.CESS_RATE)
    elss_net = elss_maturity - elss_tax

    # PPF: 15-yr lock-in, 7.1% (current), fully tax-free maturity
    ppf_rate = 0.071
    ppf_maturity = annual_investment * ((1 + ppf_rate) ** years - 1) / ppf_rate
    ppf_net = ppf_maturity  # tax-free

    # NPS: market-linked ~10%, 60% lump sum tax-free, 40% annuity (taxable)
    nps_rate = 0.10
    nps_corpus = annual_investment * ((1 + nps_rate) ** years - 1) / nps_rate
    nps_lumpsum = nps_corpus * 0.60  # tax-free
    nps_annuity = nps_corpus * 0.40  # taxable as income — approximate
    nps_net = nps_lumpsum + nps_annuity  # simplified

    return {
        'annual_investment': annual_investment,
        'years': years,
        'elss': {'maturity': round(elss_maturity), 'net_post_tax': round(elss_net),
                 'lock_in': '3 years', 'returns': '~12% (market)', 'tax_free': False},
        'ppf': {'maturity': round(ppf_maturity), 'net_post_tax': round(ppf_net),
                'lock_in': '15 years', 'returns': '7.1% (guaranteed)', 'tax_free': True},
        'nps': {'maturity': round(nps_corpus), 'net_post_tax': round(nps_net),
                'lock_in': 'Till 60', 'returns': '~10% (market)', 'tax_free': 'Partial'},
        'tax_saving_per_year': round(min(annual_investment, data.SECTION_80C_LIMIT) * marginal_rate_pct / 100 * (1 + data.CESS_RATE)),
    }


# ── T24 — EPF Maturity & Tax Calculator ──────────────────────────────────────

def calculate_epf_maturity(basic_salary, years_of_service, epf_rate=8.25):
    employee_contribution = basic_salary * 0.12
    employer_contribution = basic_salary * 0.0367  # 3.67% to EPF (rest to EPS)
    annual_contribution = (employee_contribution + employer_contribution) * 12
    rate = epf_rate / 100
    maturity = annual_contribution * ((1 + rate) ** years_of_service - 1) / rate
    # Tax: tax-free if 5+ years continuous service
    is_tax_free = years_of_service >= 5
    return {
        'basic_salary': basic_salary,
        'employee_monthly': round(employee_contribution),
        'employer_monthly': round(employer_contribution),
        'annual_contribution': round(annual_contribution),
        'years': years_of_service,
        'epf_rate': epf_rate,
        'maturity': round(maturity),
        'is_tax_free': is_tax_free,
        'tax_note': 'Fully tax-free (5+ years service)' if is_tax_free else 'Taxable — less than 5 years service. TDS @10% if PAN provided.',
    }


# ── T25 — PPF Maturity Calculator ────────────────────────────────────────────

def calculate_ppf_maturity(annual_investment, years=15, ppf_rate=7.1):
    rate = ppf_rate / 100
    if years < 15:
        # Partial withdrawal rules
        maturity = annual_investment * ((1 + rate) ** years - 1) / rate * (1 + rate)
        note = f'PPF minimum tenure is 15 years. Partial withdrawal allowed from year 7. Maturity value at year {years}.'
    else:
        maturity = annual_investment * ((1 + rate) ** years - 1) / rate * (1 + rate)
        note = 'Fully tax-free maturity. EEE investment — invest, grow, and withdraw all tax-free.'
    total_invested = annual_investment * years
    interest_earned = maturity - total_invested
    return {
        'annual_investment': annual_investment,
        'years': years,
        'ppf_rate': ppf_rate,
        'total_invested': round(total_invested),
        'interest_earned': round(interest_earned),
        'maturity': round(maturity),
        'note': note,
    }


# ── T27 — Gratuity Calculator ─────────────────────────────────────────────────

def calculate_gratuity(basic_da_salary, years_of_service, is_govt=False):
    months = years_of_service
    # Round up if 6+ months in last year
    full_years = int(months)

    if is_govt or True:  # Gratuity Act applies to establishments with 10+ employees
        # Gratuity = (Basic + DA) / 26 * 15 * Years
        gratuity = (basic_da_salary / 26) * 15 * full_years
    else:
        gratuity = (basic_da_salary / 30) * 15 * full_years

    # Tax: exempt up to ₹20L for non-govt, fully exempt for govt
    exemption_limit = None if is_govt else 2_000_000
    taxable = max(0, gratuity - exemption_limit) if exemption_limit else 0

    return {
        'basic_da_salary': basic_da_salary,
        'years_of_service': years_of_service,
        'gratuity': round(gratuity),
        'exemption_limit': exemption_limit,
        'taxable_gratuity': round(taxable),
        'tax_free_gratuity': round(gratuity - taxable),
        'is_govt': is_govt,
        'formula': 'Basic+DA ÷ 26 × 15 × Years of Service',
    }


# ── T28 — Senior Citizen Tax Calculator ──────────────────────────────────────

def calculate_senior_citizen_tax(gross_income, age_group='60_to_79',
                                  pension=0, fd_interest=0, savings_interest=0,
                                  sec_80d=0, sec_80c=0, fy='2025-26'):
    data = _get_fy_data(fy)
    # 80TTB deduction for senior citizens
    ttb = min(fd_interest + savings_interest, data.SECTION_80TTB_LIMIT)
    # 80D for senior citizens: ₹50,000
    actual_80d = min(sec_80d, data.SECTION_80D['self_family_60_plus'])

    deductions = {
        'sec_80c': sec_80c,
        'sec_80d_self': actual_80d,
        'other': ttb,
    }
    old = calculate_old_regime(gross_income, age_group, deductions, fy)
    new = calculate_new_regime(gross_income, fy)

    return {
        'gross_income': gross_income,
        'age_group': age_group,
        'ttb_deduction': round(ttb),
        'ttb_limit': data.SECTION_80TTB_LIMIT,
        'sec_80d_deduction': round(actual_80d),
        'new_regime': new,
        'old_regime': old,
        'winner': 'new' if new['total_tax'] <= old['total_tax'] else 'old',
    }


# ── T29 — Surcharge Calculator ───────────────────────────────────────────────

def calculate_surcharge(gross_income, regime='new', fy='2025-26'):
    data = _get_fy_data(fy)
    if regime == 'new':
        result = calculate_new_regime(gross_income, fy)
    else:
        result = calculate_old_regime(gross_income, fy=fy)

    surcharge_rate = 0
    for limit, rate in data.SURCHARGE_SLABS:
        if gross_income > limit:
            surcharge_rate = rate

    return {
        'gross_income': gross_income,
        'surcharge_rate': surcharge_rate * 100,
        'surcharge_amount': result['surcharge'],
        'base_tax': result['slab_tax'],
        'cess': result['cess'],
        'total_tax': result['total_tax'],
        'effective_rate': result['effective_rate'],
        'regime': regime,
    }


# ── T31 — GST Composition Scheme Calculator ───────────────────────────────────

def calculate_gst_composition(annual_turnover, business_type='trader'):
    rates = {
        'trader': 0.01,       # 1% of turnover
        'manufacturer': 0.01, # 1% of turnover
        'restaurant': 0.05,   # 5% of turnover
        'service': 0.06,      # 6% of turnover (new service provision)
    }
    limit = 1_50_00_000 if business_type != 'service' else 50_00_000
    rate = rates.get(business_type, 0.01)
    annual_tax = annual_turnover * rate
    quarterly_tax = annual_tax / 4
    eligible = annual_turnover <= limit

    return {
        'annual_turnover': annual_turnover,
        'business_type': business_type,
        'composition_rate': rate * 100,
        'annual_tax': round(annual_tax),
        'quarterly_tax': round(quarterly_tax),
        'turnover_limit': limit,
        'eligible': eligible,
        'regular_gst_estimate': round(annual_turnover * 0.18 * 0.10),  # assume 10% value add
    }


# ── T32 — GSTR Late Fee Calculator ────────────────────────────────────────────

def calculate_gstr_late_fee(return_type, days_late, has_tax_liability=True, turnover=0):
    # Late fee per day
    if return_type in ('GSTR-1', 'GSTR-3B'):
        if not has_tax_liability:
            daily_fee = 20  # nil return
        else:
            daily_fee = 50
        max_fee = 10000
        if turnover <= 1_50_00_000:
            max_fee = 2000
    elif return_type == 'GSTR-9':
        daily_fee = 200
        max_fee = min(turnover * 0.0025, 10000)
    else:
        daily_fee = 200
        max_fee = 10000

    late_fee = min(days_late * daily_fee, max_fee)
    interest = 0
    if return_type == 'GSTR-3B' and has_tax_liability and days_late > 0:
        # 18% p.a. on tax liability — simplified
        interest = round(turnover * 0.01 * days_late / 365 * 0.18)

    return {
        'return_type': return_type,
        'days_late': days_late,
        'daily_fee': daily_fee,
        'late_fee': round(late_fee),
        'interest_estimate': interest,
        'total_liability': round(late_fee + interest),
        'max_fee': round(max_fee),
    }


# ── Professional Tax Calculator ──────────────────────────────────────────────

PROFESSIONAL_TAX_SLABS = {
    'maharashtra': [(0, 7500, 0), (7501, 10000, 175), (10001, None, 200)],
    'karnataka':   [(0, 15000, 0), (15001, 29999, 150), (30000, None, 200)],
    'west-bengal': [(0, 10000, 0), (10001, 15000, 110), (15001, 25000, 130),
                    (25001, 40000, 150), (40001, None, 200)],
    'telangana':   [(0, 15000, 0), (15001, 20000, 150), (20001, None, 200)],
    'andhra-pradesh': [(0, 15000, 0), (15001, 20000, 150), (20001, None, 200)],
    'tamil-nadu':  [(0, 21000, 0), (21001, None, 182)],
    'gujarat':     [(0, 5999, 0), (6000, 8999, 80), (9000, 11999, 150), (12000, None, 200)],
    'madhya-pradesh': [(0, 18750, 0), (18751, None, 208)],
    'assam':       [(0, 10000, 0), (10001, None, 208)],
    'kerala':      [(0, 1999, 0), (2000, 2999, 20), (3000, 4999, 30), (5000, 7499, 50),
                    (7500, 9999, 75), (10000, 12499, 100), (12500, 16666, 125),
                    (16667, 20833, 166), (20834, None, 208)],
}
STATE_NAMES = {
    'maharashtra': 'Maharashtra', 'karnataka': 'Karnataka',
    'west-bengal': 'West Bengal', 'telangana': 'Telangana',
    'andhra-pradesh': 'Andhra Pradesh', 'tamil-nadu': 'Tamil Nadu',
    'gujarat': 'Gujarat', 'madhya-pradesh': 'Madhya Pradesh',
    'assam': 'Assam', 'kerala': 'Kerala',
}


def calculate_professional_tax(annual_income, state='maharashtra'):
    monthly_income = annual_income / 12
    slabs = PROFESSIONAL_TAX_SLABS.get(state, PROFESSIONAL_TAX_SLABS['maharashtra'])
    monthly_pt = 0
    for low, high, amount in slabs:
        if high is None or monthly_income <= high:
            if monthly_income >= low:
                monthly_pt = amount
            break
        if monthly_income <= high:
            monthly_pt = amount
            break
    annual_pt = monthly_pt * 12
    return {
        'annual_income': annual_income,
        'monthly_income': round(monthly_income),
        'state': state,
        'state_name': STATE_NAMES.get(state, state.replace('-', ' ').title()),
        'monthly_pt': monthly_pt,
        'annual_pt': round(annual_pt),
        'has_pt': annual_income > 0 and len(slabs) > 1,
        'note': 'Professional tax is deductible under Section 16(iii) of the Income Tax Act.',
    }


# ── NPS vs EPF Comparison ─────────────────────────────────────────────────────

def compare_nps_vs_epf(basic_salary, years=20, marginal_rate_pct=30.0):
    # EPF: employee 12% + employer 3.67% → 8.25% interest, tax-free after 5 yrs
    epf_annual = basic_salary * 0.12 * 12
    employer_epf = basic_salary * 0.0367 * 12
    epf_total_annual = epf_annual + employer_epf
    epf_rate = 0.0825
    epf_corpus = epf_total_annual * ((1 + epf_rate) ** years - 1) / epf_rate

    # NPS: assume same employee contribution, ~10% return, 60% tax-free lump sum
    nps_annual = epf_annual  # same employee contribution
    nps_rate = 0.10
    nps_corpus = nps_annual * ((1 + nps_rate) ** years - 1) / nps_rate
    nps_lump_sum_tax_free = nps_corpus * 0.60
    nps_annuity = nps_corpus * 0.40

    return {
        'basic_salary': basic_salary,
        'years': years,
        'epf': {
            'employee_monthly': round(basic_salary * 0.12),
            'employer_monthly': round(basic_salary * 0.0367),
            'annual_contribution': round(epf_total_annual),
            'corpus': round(epf_corpus),
            'net_post_tax': round(epf_corpus),
            'interest_rate': 8.25,
            'lock_in': 'Till retirement (5+ yrs for tax-free)',
            'tax_free': True,
        },
        'nps': {
            'employee_monthly': round(nps_annual / 12),
            'annual_contribution': round(nps_annual),
            'corpus': round(nps_corpus),
            'net_post_tax': round(nps_lump_sum_tax_free + nps_annuity),
            'tax_free_lump_sum': round(nps_lump_sum_tax_free),
            'annuity': round(nps_annuity),
            'interest_rate': 10.0,
            'lock_in': 'Till 60 years',
            'tax_free': 'Partial (60% lump sum)',
        },
        'winner': 'nps' if nps_corpus > epf_corpus else 'epf',
    }


# ── Tax Saving Checklist Generator ────────────────────────────────────────────

def generate_tax_checklist(gross_income, regime='new', has_hra=False,
                            sec_80c_invested=0, has_health_insurance=False,
                            has_home_loan=False, has_nps=False, fy='2025-26'):
    data = _get_fy_data(fy)
    items = []
    potential_saving = 0

    if regime == 'old':
        remaining_80c = max(0, data.SECTION_80C_LIMIT - sec_80c_invested)
        if remaining_80c > 0:
            saving = remaining_80c * 0.30 * (1 + data.CESS_RATE)
            items.append({
                'priority': 'high',
                'section': '80C',
                'action': f'Invest ₹{remaining_80c:,} more in ELSS/PPF/NPS to use full 80C limit',
                'saving': round(saving),
                'done': False,
            })
            potential_saving += saving

        if not has_health_insurance:
            saving = 25000 * 0.30 * (1 + data.CESS_RATE)
            items.append({
                'priority': 'high',
                'section': '80D',
                'action': 'Buy health insurance (₹25,000 deduction available)',
                'saving': round(saving),
                'done': False,
            })
            potential_saving += saving

        if not has_nps:
            saving = data.SECTION_80CCD_1B * 0.30 * (1 + data.CESS_RATE)
            items.append({
                'priority': 'medium',
                'section': '80CCD(1B)',
                'action': 'Invest ₹50,000 in NPS for extra deduction beyond 80C',
                'saving': round(saving),
                'done': False,
            })
            potential_saving += saving

        if has_hra and gross_income > 600000:
            items.append({
                'priority': 'medium',
                'section': 'HRA',
                'action': 'Claim HRA exemption — submit rent receipts to employer',
                'saving': 0,
                'done': False,
            })

    if regime == 'new' and gross_income <= data.NEW_REGIME_REBATE_LIMIT:
        items.append({
            'priority': 'high',
            'section': '87A Rebate',
            'action': 'Your income is within ₹12L — you pay ZERO tax under New Regime!',
            'saving': 0,
            'done': True,
        })

    items.append({
        'priority': 'low',
        'section': 'Advance Tax',
        'action': 'Calculate and pay advance tax by due dates to avoid interest',
        'saving': 0,
        'done': False,
    })

    return {
        'gross_income': gross_income,
        'regime': regime,
        'items': items,
        'total_potential_saving': round(potential_saving),
        'items_count': len(items),
        'fy': fy,
    }


# ── T35 — 80E Education Loan Interest ────────────────────────────────────────

def calculate_80e_benefit(annual_interest, loan_year, marginal_rate_pct=30.0, fy='2025-26'):
    data = _get_fy_data(fy)
    # 80E: No monetary limit. Available for 8 years from first repayment year.
    max_years = 8
    if loan_year > max_years:
        deduction = 0
        note = f'80E deduction not available. Limit is {max_years} years from first EMI.'
    else:
        deduction = annual_interest
        years_remaining = max_years - loan_year + 1
        note = f'80E available for {years_remaining} more year(s). No upper limit on amount.'
    tax_saved = deduction * (marginal_rate_pct / 100) * (1 + data.CESS_RATE)
    return {
        'annual_interest': annual_interest,
        'loan_year': loan_year,
        'deduction': round(deduction),
        'tax_saved': round(tax_saved),
        'max_years': max_years,
        'note': note,
        'marginal_rate_pct': marginal_rate_pct,
    }
