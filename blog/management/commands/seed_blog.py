from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import Author, Category, Article
from tools.models import Tool


ARTICLES = [
    {
        'title': 'Old vs New Tax Regime: Which Is Better for You in FY 2025-26?',
        'slug': 'old-vs-new-tax-regime-which-is-better-fy-2025-26',
        'category': 'income-tax',
        'tags': 'old regime,new regime,tax regime,FY 2025-26',
        'excerpt': 'Confused between old and new tax regime? We compare both regimes with real salary examples, deduction impact, and a clear verdict for FY 2025-26.',
        'meta_title': 'Old vs New Tax Regime FY 2025-26: Which Is Better?',
        'meta_description': 'Compare old vs new tax regime for FY 2025-26. See which saves more tax for your salary with real examples and our free calculator.',
        'reading_time': 8,
        'is_featured': True,
        'tool_slug': 'old-vs-new-tax-regime',
        'body': '''## Old vs New Tax Regime FY 2025-26

The choice between old and new tax regime is the single most important tax decision for most salaried Indians in FY 2025-26.

## New Regime — FY 2025-26 Slabs

| Income Slab | Tax Rate |
|---|---|
| Up to ₹4,00,000 | 0% |
| ₹4,00,001 – ₹8,00,000 | 5% |
| ₹8,00,001 – ₹12,00,000 | 10% |
| ₹12,00,001 – ₹16,00,000 | 15% |
| ₹16,00,001 – ₹20,00,000 | 20% |
| ₹20,00,001 – ₹24,00,000 | 25% |
| Above ₹24,00,000 | 30% |

**Key benefit:** Income up to ₹12,00,000 = zero tax (after ₹75,000 standard deduction + Section 87A rebate of ₹60,000).

## Old Regime — FY 2025-26 Slabs (Below 60)

| Income Slab | Tax Rate |
|---|---|
| Up to ₹2,50,000 | 0% |
| ₹2,50,001 – ₹5,00,000 | 5% |
| ₹5,00,001 – ₹10,00,000 | 20% |
| Above ₹10,00,000 | 30% |

**Key benefit:** You can claim 80C (₹1.5L), 80D (₹25K), HRA, NPS, home loan interest, and many more deductions.

## When New Regime Wins

- Your deductions are below ₹3.75 lakh
- You don't claim HRA (living in own house or parents' house)
- You're a fresher without 80C investments yet
- You want simplicity — no investment proofs required

## When Old Regime Wins

- You claim HRA + 80C + 80D + NPS = total deductions above ₹3.75L
- You have a home loan with large interest component
- Senior citizens with 80TTB + 80D benefits

## Quick Verdict by Salary

| Annual CTC | Recommended Regime |
|---|---|
| Up to ₹12L | New Regime (zero tax) |
| ₹12L–₹15L | Depends on deductions |
| Above ₹15L with max deductions | Old Regime likely better |
| Above ₹15L, minimal deductions | New Regime |

## Use Our Calculator

Use the [Old vs New Regime Calculator](/tools/old-vs-new-tax-regime/) to enter your exact salary and deductions — it shows the winner instantly.

## Frequently Asked Questions

**Can I switch regime every year?**
Yes — salaried employees can switch every year. Business income earners can switch only once from old to new.

**Is standard deduction available in new regime?**
Yes — ₹75,000 standard deduction is available in the new regime from FY 2025-26.

**What is the rebate limit in new regime?**
Under Section 87A, income up to ₹12L is fully rebated. So net tax = 0 for income ≤ ₹12,75,000 (after ₹75K standard deduction).
''',
    },
    {
        'title': 'Income Tax Slabs FY 2025-26: Complete Guide (Old + New Regime)',
        'slug': 'income-tax-slabs-fy-2025-26-old-new-regime',
        'category': 'income-tax',
        'tags': 'income tax slabs,FY 2025-26,tax rates,budget 2025',
        'excerpt': 'Complete income tax slab rates for FY 2025-26 (AY 2026-27) — both old and new regime, with cess, surcharge, and rebate limits explained.',
        'meta_title': 'Income Tax Slabs FY 2025-26: Old & New Regime Rates',
        'meta_description': 'Income tax slab rates for FY 2025-26. Old regime slabs, new regime slabs, 4% cess, surcharge, and Section 87A rebate explained with examples.',
        'reading_time': 7,
        'body': '''## Income Tax Slabs FY 2025-26 (AY 2026-27)

Budget 2025 brought major changes to the new tax regime. Here are the complete slab rates.

## New Regime Slabs — FY 2025-26

| Taxable Income | Rate |
|---|---|
| Up to ₹4,00,000 | Nil |
| ₹4L – ₹8L | 5% |
| ₹8L – ₹12L | 10% |
| ₹12L – ₹16L | 15% |
| ₹16L – ₹20L | 20% |
| ₹20L – ₹24L | 25% |
| Above ₹24L | 30% |

Standard deduction: ₹75,000
Section 87A rebate: Up to ₹60,000 (income ≤ ₹12L after std deduction)

## Old Regime Slabs — FY 2025-26

**Below 60 years:**

| Income | Rate |
|---|---|
| Up to ₹2,50,000 | Nil |
| ₹2.5L – ₹5L | 5% |
| ₹5L – ₹10L | 20% |
| Above ₹10L | 30% |

**Senior Citizens (60–79):** Nil up to ₹3L
**Super Senior (80+):** Nil up to ₹5L

## Cess & Surcharge

- **Health & Education Cess:** 4% on total tax
- **Surcharge:** Applies on income above ₹50L

| Income | Surcharge Rate |
|---|---|
| ₹50L – ₹1Cr | 10% |
| ₹1Cr – ₹2Cr | 15% |
| ₹2Cr – ₹5Cr | 25% |
| Above ₹5Cr | 37% (old) / 25% (new) |

## Example: ₹15L Salary (New Regime)

- Gross income: ₹15,00,000
- Less standard deduction: ₹75,000
- Taxable income: ₹14,25,000
- Tax: ₹0 (4L) + ₹20,000 (4L@5%) + ₹40,000 (4L@10%) + ₹33,750 (2.25L@15%)
- Total tax: ₹93,750
- Plus 4% cess: ₹3,750
- **Total: ₹97,500**

Use our [Income Tax Calculator](/tools/income-tax-calculator/) for instant results.
''',
    },
    {
        'title': 'HRA Exemption Calculation: Formula, Example, Calculator',
        'slug': 'hra-exemption-calculation-formula-example',
        'category': 'deductions',
        'tags': 'HRA,house rent allowance,HRA exemption,Section 10(13A)',
        'excerpt': 'Learn the exact HRA exemption formula, see a worked example for metro and non-metro cities, and use our free HRA calculator for FY 2025-26.',
        'meta_title': 'HRA Exemption Calculator FY 2025-26: Formula & Example',
        'meta_description': 'Calculate HRA exemption under Section 10(13A). Three-condition formula explained with metro and non-metro examples. Free HRA calculator.',
        'reading_time': 6,
        'tool_slug': 'hra-exemption-calculator',
        'body': '''## HRA Exemption — Section 10(13A)

HRA (House Rent Allowance) exemption is one of the biggest tax savers for salaried employees in rented accommodation.

**Only available under Old Regime.**

## The Three-Condition Formula

HRA exemption = Minimum of:

1. **Actual HRA received** from employer
2. **50% of Basic** (metro) or **40% of Basic** (non-metro)
3. **Actual rent paid minus 10% of Basic**

Metro cities: Delhi, Mumbai, Chennai, Kolkata

## Example 1 — Metro City (Mumbai)

| | Amount |
|---|---|
| Basic Salary | ₹50,000/mo |
| HRA Received | ₹25,000/mo |
| Rent Paid | ₹22,000/mo |
| City | Mumbai (Metro) |

Calculation:
1. HRA received: ₹25,000
2. 50% of Basic: ₹25,000
3. Rent – 10% of Basic: ₹22,000 – ₹5,000 = ₹17,000

**HRA Exemption = ₹17,000/mo = ₹2,04,000/yr**

## Example 2 — Non-Metro (Pune)

| | Amount |
|---|---|
| Basic Salary | ₹50,000/mo |
| HRA Received | ₹20,000/mo |
| Rent Paid | ₹15,000/mo |
| City | Pune (Non-Metro) |

Calculation:
1. HRA received: ₹20,000
2. 40% of Basic: ₹20,000
3. Rent – 10% of Basic: ₹15,000 – ₹5,000 = ₹10,000

**HRA Exemption = ₹10,000/mo = ₹1,20,000/yr**

## Documents Required

- Rent receipts (monthly, signed by landlord)
- Rent agreement
- Landlord PAN (if annual rent > ₹1L)

## Common Mistakes

- Claiming HRA in new tax regime (not allowed)
- Not deducting 10% of basic from rent
- Paying rent to spouse (not allowed)

Use the [HRA Calculator](/tools/hra-exemption-calculator/) for instant calculation.
''',
    },
    {
        'title': 'Section 80C Deductions: Complete List and Limits for FY 2025-26',
        'slug': 'section-80c-deductions-complete-list-fy-2025-26',
        'category': 'deductions',
        'tags': '80C,deductions,tax saving,ELSS,PPF,LIC,EPF',
        'excerpt': 'Complete list of Section 80C investments and deductions for FY 2025-26 — ELSS, PPF, LIC, EPF, NSC, home loan principal, tuition fees, and more.',
        'meta_title': 'Section 80C Deductions: Complete List FY 2025-26',
        'meta_description': 'All Section 80C deductions for FY 2025-26. ₹1.5 lakh limit, ELSS vs PPF vs LIC comparison, best investments to maximise your 80C savings.',
        'reading_time': 9,
        'tool_slug': '80c-deduction-calculator',
        'body': '''## Section 80C — ₹1,50,000 Deduction

Section 80C is the most popular tax-saving section. You can deduct up to ₹1,50,000 from your taxable income.

**Only available under Old Regime.**

## Complete 80C Investment List

| Investment | Lock-in | Returns | Risk |
|---|---|---|---|
| ELSS Mutual Fund | 3 years | 12–15% (market) | High |
| PPF | 15 years | 7.1% (guaranteed) | None |
| EPF (employee share) | Until retirement | 8.25% | None |
| NSC | 5 years | 7.7% | None |
| 5-Year FD (tax-saver) | 5 years | 6.5–7.5% | None |
| NPS (Tier 1) | Until 60 | Market-linked | Medium |
| Sukanya Samriddhi | Until daughter 21 | 8.2% | None |
| LIC / Term Insurance premium | Policy term | Risk cover | None |
| ULIP | 5 years | Market-linked | Medium |

## 80C Deductions (Non-Investment)

- Home loan **principal** repayment
- Children's tuition fees (up to 2 children, full-time)
- Stamp duty + registration on new house (year of purchase only)

## Best 80C Picks for FY 2025-26

**For tax saving + wealth creation:** ELSS (3-year lock-in, highest returns)
**For guaranteed returns:** PPF (15-year lock-in, tax-free maturity)
**For senior citizens:** 5-year tax-saver FD (safe, fixed returns)
**For daughters:** Sukanya Samriddhi (8.2% guaranteed, fully tax-free)

## Tax Saving Calculation

₹1,50,000 in 80C + you're in 30% bracket:
- Tax saved = ₹1,50,000 × 30% = ₹45,000
- Plus 4% cess = ₹1,800 saved
- **Total tax saved: ₹46,800**

## Beyond 80C

After exhausting 80C, look at:
- **80CCD(1B):** Additional ₹50,000 in NPS
- **80D:** Up to ₹25,000 health insurance premium
- **Section 24(b):** Home loan interest up to ₹2L

Use the [80C Planner](/tools/80c-deduction-calculator/) to optimise your deductions.
''',
    },
    {
        'title': 'Advance Tax: Who Should Pay, Due Dates, How to Calculate',
        'slug': 'advance-tax-who-should-pay-due-dates-how-to-calculate',
        'category': 'income-tax',
        'tags': 'advance tax,TDS,tax payment,due dates,Section 208',
        'excerpt': 'Who must pay advance tax, the four due dates in FY 2025-26, how to calculate quarterly instalments, and penalty for non-payment under Section 234B/C.',
        'meta_title': 'Advance Tax FY 2025-26: Due Dates, Calculation & Payment',
        'meta_description': 'Advance tax guide for FY 2025-26. Who pays, 4 due dates (Jun 15, Sep 15, Dec 15, Mar 15), how to calculate, and Section 234B/C penalties.',
        'reading_time': 7,
        'tool_slug': 'advance-tax-calculator',
        'body': '''## What Is Advance Tax?

Advance tax is income tax paid in advance during the financial year, rather than as a lump sum at year-end.

## Who Must Pay Advance Tax?

Any individual whose estimated tax liability for the year **exceeds ₹10,000** after deducting TDS.

**Exceptions:**
- Senior citizens (60+) with no business income — exempt
- Salaried employees where TDS covers full liability — generally exempt

## Advance Tax Due Dates — FY 2025-26

| Instalment | Due Date | Percentage of Tax |
|---|---|---|
| 1st | 15 June 2025 | 15% |
| 2nd | 15 September 2025 | 45% |
| 3rd | 15 December 2025 | 75% |
| 4th | 15 March 2026 | 100% |

## Calculation Example

Annual tax liability: ₹1,20,000

| Date | Cumulative % | Amount to Pay |
|---|---|---|
| By Jun 15 | 15% | ₹18,000 |
| By Sep 15 | 45% | ₹54,000 – ₹18,000 = ₹36,000 |
| By Dec 15 | 75% | ₹90,000 – ₹54,000 = ₹36,000 |
| By Mar 15 | 100% | ₹1,20,000 – ₹90,000 = ₹30,000 |

## Interest Penalty for Non-Payment

**Section 234B:** If advance tax < 90% of total tax — 1% per month interest
**Section 234C:** For each instalment shortfall — 1% per month for 3 months

## How to Pay Advance Tax

1. Go to [incometax.gov.in](https://www.incometax.gov.in)
2. Select Challan 280
3. Choose "Advance Tax (100)"
4. Pay online via net banking / UPI / debit card

Use the [Advance Tax Calculator](/tools/advance-tax-calculator/) to find your exact quarterly amounts.
''',
    },
    {
        'title': 'CTC vs Take-Home Salary: What\'s the Difference?',
        'slug': 'ctc-vs-take-home-salary-difference-explained',
        'category': 'income-tax',
        'tags': 'CTC,take home salary,in-hand salary,PF,TDS,professional tax',
        'excerpt': 'Your CTC and take-home salary can differ by 20–40%. Here\'s exactly what gets deducted — PF, TDS, professional tax, gratuity — with a real example.',
        'meta_title': 'CTC vs Take-Home Salary: Difference Explained with Example',
        'meta_description': 'CTC ₹12L but take-home only ₹80K? Learn what gets deducted — PF, TDS, professional tax, gratuity. Free CTC to take-home calculator.',
        'reading_time': 6,
        'body': '''## CTC vs Take-Home: The Gap

Many employees are surprised to find their monthly take-home is 20–35% less than CTC/12. Here's why.

## CTC (Cost to Company)

CTC = everything your employer spends on you:
- Basic salary
- HRA
- Special allowances
- Employer PF contribution (12% of basic)
- Gratuity provision (~4.8% of basic)
- Medical insurance premium
- Food coupons / sodexo
- Bonus

## What Gets Deducted from Gross Salary

| Deduction | Amount |
|---|---|
| Employee PF | 12% of basic |
| Professional Tax | ₹200–₹2,400/yr (state-wise) |
| TDS (income tax) | Based on regime and investments |
| ESI (if salary < ₹21K/mo) | 0.75% of gross |

## Example: ₹12L CTC

| Component | Annual | Monthly |
|---|---|---|
| Basic | ₹5,40,000 | ₹45,000 |
| HRA (50% of basic) | ₹2,70,000 | ₹22,500 |
| Special Allowance | ₹1,01,400 | ₹8,450 |
| Employer PF | ₹64,800 | ₹5,400 |
| Gratuity | ₹25,962 | ₹2,163 |
| **CTC Total** | **₹12,02,162** | **₹1,00,180** |

**Deductions:**
- Employee PF: ₹5,400
- Professional Tax: ₹200
- TDS (new regime): ~₹0 (₹12L = zero tax)

**Take-home: ~₹75,350/month**

## Tips to Maximise Take-Home

- Submit rent receipts → claim HRA exemption (old regime)
- Use NPS corporate contribution (no employee tax)
- Choose Flexi Benefit Plan wisely (medical, books, fuel)

Calculate your exact take-home with our [CTC to Take-Home Calculator](/tools/ctc-to-take-home/).
''',
    },
    {
        'title': 'Capital Gains Tax on Mutual Funds After Budget 2024',
        'slug': 'capital-gains-tax-mutual-funds-budget-2024',
        'category': 'investments',
        'tags': 'capital gains,mutual funds,STCG,LTCG,Budget 2024,equity funds',
        'excerpt': 'Budget 2024 changed STCG and LTCG rates on mutual funds. Here are the new rates, grandfathering provisions, and examples for equity and debt funds.',
        'meta_title': 'Capital Gains Tax on Mutual Funds After Budget 2024',
        'meta_description': 'STCG 20%, LTCG 12.5% on equity mutual funds after Budget 2024. New rates, ₹1.25L exemption, debt fund indexation removed. Full guide.',
        'reading_time': 8,
        'tool_slug': 'capital-gains-calculator',
        'body': '''## Capital Gains Tax — Post Budget 2024

Budget 2024 significantly changed capital gains taxation. Here's what changed.

## Equity Mutual Funds & Stocks

| Holding Period | Old Rate | New Rate (Budget 2024) |
|---|---|---|
| < 12 months (STCG) | 15% | **20%** |
| > 12 months (LTCG) | 10% above ₹1L | **12.5% above ₹1.25L** |

Changes effective: 23 July 2024

## LTCG Exemption Increase

Good news: LTCG exemption increased from ₹1,00,000 to **₹1,25,000** per year.

So gains up to ₹1,25,000/year on equity = **zero tax**.

## Example: LTCG Calculation

- Buy: ₹5,00,000 (January 2023)
- Sell: ₹7,50,000 (August 2024)
- Gain: ₹2,50,000
- Exemption: ₹1,25,000
- Taxable gain: ₹1,25,000
- Tax @12.5%: **₹15,625**

## Debt Mutual Funds — Big Change

From April 2023, debt fund gains are taxed as **ordinary income** (slab rate).
- No LTCG benefit anymore
- No indexation benefit (removed Budget 2024 for all assets)
- Effectively: debt funds taxed same as FD

## Hybrid Funds

Depends on equity allocation:
- Equity > 65%: equity taxation rules apply
- Equity < 65%: debt taxation rules apply

## Tax Harvesting Strategy

Sell and rebuy equity funds every year to realise LTCG within ₹1,25,000 limit.
- Zero tax on gains
- Resets your cost base higher
- Reduces future LTCG tax

Use the [Capital Gains Calculator](/tools/capital-gains-calculator/) to compute your exact tax.
''',
    },
    {
        'title': 'GST for Freelancers: When You Must Register, What to File',
        'slug': 'gst-for-freelancers-registration-filing-guide',
        'category': 'gst',
        'tags': 'GST,freelancer,GST registration,threshold,GSTR-1,GSTR-3B',
        'excerpt': 'Should you register for GST as a freelancer? The ₹20L threshold, what counts as interstate supply, how to file GSTR-1 and GSTR-3B, and ITR-4 tips.',
        'meta_title': 'GST for Freelancers India: Registration, Filing Guide 2025',
        'meta_description': 'GST guide for freelancers. ₹20L threshold, interstate clients mandatory GST, GSTR-1 and GSTR-3B filing, input credit on expenses. FY 2025-26.',
        'reading_time': 8,
        'body': '''## GST Registration for Freelancers

### Mandatory Registration

You **must** register for GST if:
- Annual turnover exceeds **₹20 lakh** (services)
- You supply services to clients in **another state** (interstate = mandatory regardless of turnover)
- You sell on e-commerce platforms

**North-East & Special Category States:** Threshold is ₹10L

### Voluntary Registration

Register voluntarily if you have large business expenses — you can claim **Input Tax Credit (ITC)** on GST paid on your purchases.

## GST Rate on Freelance Services

Most freelance services (IT, design, writing, consulting) = **18% GST**

If you invoice ₹1,00,000 to a client, add ₹18,000 GST = total invoice ₹1,18,000.

## Returns to File

| Return | What | Frequency |
|---|---|---|
| GSTR-1 | Sales invoices | Monthly/Quarterly |
| GSTR-3B | Summary + tax payment | Monthly |
| GSTR-9 | Annual return | Yearly |

**Quarterly filers:** If annual turnover < ₹5Cr, you can file GSTR-1 quarterly (QRMP scheme) but must pay tax monthly.

## Input Tax Credit for Freelancers

You can claim ITC on:
- Laptop, monitor, hardware (18% GST)
- Internet connection (18%)
- Software subscriptions (18%)
- Office rent (if landlord is GST registered)
- Professional services (CA fees, etc.)

## Reverse Charge for Foreign Clients

If your client is outside India, GST = 0% (zero-rated export of service).
- File a **LUT (Letter of Undertaking)** — avoids paying GST upfront
- Show in GSTR-1 as zero-rated supply
- Still eligible for ITC refund on expenses

## Composition Scheme — Freelancers

Not available for service providers (except restaurants). Freelancers cannot opt for composition.

## ITR for Freelancers with GST

- Use ITR-3 (business income) or ITR-4 (44ADA presumptive)
- Report GST turnover (excluding GST collected — that's not your income)
- 44ADA: 50% of gross receipts = presumptive income

Use the [GST Calculator](/gst/gst-calculator/) to compute invoice amounts.
''',
    },
    {
        'title': 'Income Tax for Salaried Employees: Complete Guide FY 2025-26',
        'slug': 'income-tax-for-salaried-employees-complete-guide-fy-2025-26',
        'category': 'income-tax',
        'tags': 'salaried employees,income tax,TDS,Form 16,ITR-1,tax guide',
        'excerpt': 'End-to-end income tax guide for salaried employees in FY 2025-26: how TDS works, how to choose regime, claim deductions, and file ITR-1.',
        'meta_title': 'Income Tax for Salaried Employees: Complete Guide FY 2025-26',
        'meta_description': 'Salaried employee tax guide FY 2025-26. TDS, Form 16, old vs new regime, 80C/HRA deductions, ITR-1 filing. Everything in one place.',
        'reading_time': 10,
        'body': '''## Income Tax for Salaried Employees — FY 2025-26

If you're salaried, your employer deducts TDS every month and pays it to the government. But you still need to file ITR and may get a refund — or pay more.

## Step 1: Understand Your Salary Structure

Ask HR for your **salary breakup**:
- Basic salary (usually 40–50% of CTC)
- HRA (usually 40–50% of basic)
- Special allowance (balancing figure)
- Employer PF (12% of basic — not your income)

## Step 2: Choose Your Tax Regime

**New Regime (default from FY 2023-24):**
- Standard deduction: ₹75,000
- No other deductions
- Zero tax if income ≤ ₹12,75,000

**Old Regime:**
- Claim HRA, 80C, 80D, NPS, home loan interest
- Better if total deductions > ₹3.75L

Inform employer your regime choice before April — they'll deduct TDS accordingly.

## Step 3: Submit Investment Proofs (Old Regime)

By January–February, submit:
- Rent receipts (for HRA)
- 80C investment proofs (ELSS, PPF, LIC)
- Health insurance premium receipt (80D)
- Home loan interest certificate

Employer adjusts TDS for remaining months.

## Step 4: Verify Form 26AS and AIS

- **Form 26AS**: TDS deposited by employer, banks, others
- **AIS (Annual Information Statement)**: All financial transactions
- Download from incometax.gov.in → Your profile

Both should match your salary and investment records. Discrepancy = potential notice.

## Step 5: Collect Form 16

Form 16 = employer's TDS certificate. Two parts:
- **Part A**: TDS deposited month-wise
- **Part B**: Salary breakup, deductions, tax computed

Available from employer by June 15.

## Step 6: File ITR-1

Salaried employees with:
- Salary income
- Interest income
- One house property

...file **ITR-1 (Sahaj)**.

Use ITR-2 if you have capital gains.

File by **July 31** (AY 2026-27).

## Common Mistakes to Avoid

- Forgetting to report interest from savings account (taxable above ₹10,000)
- Not claiming HRA exemption in old regime
- Not submitting Form 15G/15H for FDs (if no tax liability)
- Missing the ITR deadline (₹5,000 late fee)

Use the [Income Tax Calculator](/tools/income-tax-calculator/) to estimate your tax.
''',
    },
    {
        'title': '44ADA Presumptive Taxation for Professionals: Is It Right for You?',
        'slug': 'section-44ada-presumptive-tax-professionals-guide',
        'category': 'freelancer',
        'tags': '44ADA,presumptive tax,professionals,CA,doctor,freelancer,ITR-4',
        'excerpt': 'Section 44ADA allows professionals to pay tax on 50% of gross receipts without maintaining books. Is it better than actual expenses? Complete guide.',
        'meta_title': 'Section 44ADA Presumptive Tax for Professionals: Complete Guide',
        'meta_description': 'Section 44ADA guide: who qualifies, 50% presumptive income, new vs old regime comparison, when actual books are better. Free 44ADA calculator.',
        'reading_time': 7,
        'tool_slug': 'presumptive-tax-44ada',
        'body': '''## Section 44ADA — Presumptive Taxation for Professionals

Section 44ADA simplifies taxation for eligible professionals. Instead of maintaining books of accounts, you declare 50% of gross receipts as income.

## Who Qualifies?

Professionals in specified categories **with annual gross receipts ≤ ₹75 lakh**:

- Doctors (medical)
- Lawyers and advocates
- Engineers
- Chartered Accountants (CA)
- Company Secretaries (CS)
- Architects
- Interior decorators
- Technical consultants
- IT professionals (consulting services)

## How It Works

**Simple formula:** Taxable Income = 50% × Gross Receipts

**Example:**
- CA practice gross receipts: ₹30,00,000
- Presumptive income: ₹15,00,000
- No books of accounts required
- No expense tracking needed

## 44ADA vs Actual Expenses — When to Choose Which

### Choose 44ADA if:
- Your actual expenses < 50% of receipts
- You don't want bookkeeping hassle
- You're a solo professional without high office costs

### Choose Actual Books if:
- Your actual expenses > 50% of receipts
- You have significant depreciation (equipment, vehicles)
- Your net profit is less than 50% of revenue

## Tax Comparison: ₹30L Receipts

| | 44ADA | Actual (60% expenses) |
|---|---|---|
| Gross Receipts | ₹30L | ₹30L |
| Taxable Income | ₹15L | ₹12L |
| Tax (New Regime) | ~₹1.05L | ~₹48K |

In this example, actual books saves ~₹57,000.

## Advance Tax under 44ADA

Unlike general business (44AD), professionals under 44ADA must pay advance tax in 4 instalments like any individual.

If annual tax < ₹10,000: no advance tax required.

## ITR Form to Use

File **ITR-4 (Sugam)** — designed for presumptive taxation.

## Key Condition

If you opt for 44ADA, you cannot claim:
- Depreciation (already assumed to be in the 50%)
- Any specific business expense

But you can still claim Chapter VI-A deductions (80C, 80D, etc.) in old regime.

Use the [44ADA Calculator](/tools/presumptive-tax-44ada/) to compare regimes.
''',
    },
    {
        'title': 'Section 80D: How Much Tax Can You Save on Health Insurance?',
        'slug': 'section-80d-health-insurance-tax-saving-guide',
        'category': 'deductions',
        'tags': '80D,health insurance,mediclaim,preventive health checkup,senior citizen',
        'excerpt': 'Section 80D allows deduction on health insurance premium for self, family, and parents. Limits for senior citizens, preventive checkup, and examples.',
        'meta_title': 'Section 80D: Tax Saving on Health Insurance FY 2025-26',
        'meta_description': 'Section 80D deduction limits: ₹25K self+family, ₹50K senior parents. Preventive health checkup ₹5K included. Examples and calculator for FY 2025-26.',
        'reading_time': 6,
        'body': '''## Section 80D — Health Insurance Deduction

Section 80D lets you deduct health insurance premiums from your taxable income. **Available only under Old Regime.**

## Deduction Limits

| Coverage | Under 60 | 60+ (Senior) |
|---|---|---|
| Self + Spouse + Children | ₹25,000 | ₹50,000 |
| Parents (under 60) | ₹25,000 | — |
| Parents (Senior Citizen, 60+) | — | ₹50,000 |

**Maximum possible deduction:**
- Self + family (non-senior) + senior parents = ₹25,000 + ₹50,000 = **₹75,000**
- Self (senior) + senior parents = ₹50,000 + ₹50,000 = **₹1,00,000**

## Preventive Health Checkup

₹5,000 included within the above limits (not over and above).

So if you pay ₹20,000 insurance premium + ₹5,000 checkup = ₹25,000 total (hits limit for self).

## Example Calculation

Ravi, 35 years, old regime:
- Health insurance for self + wife + 2 kids: ₹18,000/year
- Health insurance for parents (both 62): ₹42,000/year
- Preventive checkup: ₹3,000

80D deduction:
- Self + family: min(₹18,000 + ₹3,000, ₹25,000) = ₹21,000
- Senior parents: min(₹42,000, ₹50,000) = ₹42,000
- **Total 80D: ₹63,000**

Tax saved (30% bracket): ₹63,000 × 30% = ₹18,900 + 4% cess = ~₹19,656 saved

## Cash Payment Rule

Premiums paid in **cash** are NOT eligible for 80D.
Must pay via cheque / online / UPI.

(Exception: preventive health checkup up to ₹5,000 cash is allowed)

## Group Health Insurance from Employer

If employer provides group mediclaim:
- Premium paid by employer = not eligible for 80D
- Premium paid by employee (top-up cover) = eligible for 80D

## What's NOT Covered

- Life insurance premium (that's 80C)
- OPD expenses without an insurance policy
- GST on health insurance premium
''',
    },
    {
        'title': 'Home Loan Tax Benefit: Section 24, 80C, 80EEA Explained',
        'slug': 'home-loan-tax-benefit-section-24-80c-80eea-explained',
        'category': 'deductions',
        'tags': 'home loan,Section 24,80C,80EEA,tax benefit,housing loan interest',
        'excerpt': 'A home loan gives you three tax benefits: ₹2L interest deduction (Sec 24), ₹1.5L principal (80C), and ₹1.5L for affordable housing (80EEA). Explained with examples.',
        'meta_title': 'Home Loan Tax Benefits: Section 24, 80C & 80EEA Guide',
        'meta_description': 'Home loan tax benefits: ₹2L under Section 24(b), ₹1.5L principal under 80C, extra ₹1.5L under 80EEA for first home. Old regime only. Examples.',
        'reading_time': 7,
        'body': '''## Home Loan Tax Benefits — Three Sections

A home loan gives you deductions under **three separate sections** of the Income Tax Act. All available under **Old Regime only**.

## Section 24(b) — Interest Deduction

- **Self-occupied property:** Deduction up to **₹2,00,000/year** on home loan interest
- **Let-out property:** Full interest deductible (no cap), but set-off against salary capped at ₹2L; rest carried forward 8 years

**Condition:** Property construction must complete within 5 years of loan.

## Section 80C — Principal Repayment

- Deduction up to **₹1,50,000/year** on principal repaid
- Included within the overall 80C limit (not separate)
- Also includes stamp duty + registration costs (only in year of purchase)

**Condition:** Don't sell the house within 5 years (deductions reversed if sold).

## Section 80EEA — First-Time Buyer Bonus

- Extra **₹1,50,000/year** on home loan interest
- **Over and above** Section 24(b) — total interest deduction = ₹3.5L
- Only for first-time home buyers
- Loan sanctioned between April 2019 – March 2022 (check if extended)
- Stamp duty value of property ≤ ₹45 lakh

## Example: ₹50L Home Loan @ 8.5%

Annual interest (Year 1): ~₹4,20,000
Annual principal: ~₹60,000

| Section | Deduction | Tax Saved (30%) |
|---|---|---|
| 24(b) Interest | ₹2,00,000 | ₹60,000 |
| 80C Principal | ₹60,000 | ₹18,000 |
| **Total** | **₹2,60,000** | **₹78,000** |

If 80EEA applies: additional ₹1.5L → tax saved = ₹78,000 + ₹45,000 = ₹1,23,000

## Joint Home Loan — Double Benefit

If husband + wife are joint borrowers and co-owners:
- Each claims ₹2L under 24(b) = ₹4L total interest deduction
- Each claims 80C principal share
- Effectively doubles the tax benefit

## Pre-EMI Interest

During construction period, interest paid as pre-EMI is deductible in 5 equal instalments starting from the year of possession.
''',
    },
    {
        'title': 'NPS Tax Benefits: All Sections Explained (80CCD1, 80CCD1B, 80CCD2)',
        'slug': 'nps-tax-benefits-sections-80ccd1-80ccd1b-80ccd2-explained',
        'category': 'deductions',
        'tags': 'NPS,National Pension System,80CCD,tax benefit,retirement,80CCD1B',
        'excerpt': 'NPS gives tax benefits under three sections: 80CCD(1) within 80C, extra ₹50K under 80CCD(1B), and employer contribution under 80CCD(2). All explained.',
        'meta_title': 'NPS Tax Benefits: 80CCD(1), 80CCD(1B), 80CCD(2) Explained',
        'meta_description': 'NPS tax benefits: ₹1.5L under 80CCD(1), extra ₹50K under 80CCD(1B), employer NPS under 80CCD(2). Maximise ₹2L+ deduction. FY 2025-26 guide.',
        'reading_time': 7,
        'body': '''## NPS Tax Benefits — Three Sections

National Pension System (NPS) is unique in offering deductions under **three separate sections**. Understanding all three maximises your tax saving.

## Section 80CCD(1) — Employee Contribution (Within 80C)

- Deduction up to **10% of salary** (basic + DA) or ₹1,50,000, whichever is lower
- **Part of the overall 80C limit of ₹1.5L** — not separate

Most people use 80C for ELSS/PPF, so NPS under 80CCD(1) competes with those.

## Section 80CCD(1B) — Extra ₹50,000 (Best Part!)

- Additional deduction of **₹50,000** per year
- **Over and above** the 80C limit of ₹1.5L
- Available in **Old Regime only**
- This is the most valuable NPS deduction — pure additional saving

**Tax saved on ₹50,000 (30% bracket):** ₹50,000 × 30% × 1.04 = **₹15,600**

## Section 80CCD(2) — Employer's NPS Contribution

- Employer's contribution to your NPS is deductible
- Up to **14% of salary** (Basic + DA) for central government employees
- Up to **10% of salary** for private sector employees
- **No monetary cap** (just % limit)
- Available in **both Old and New Regime** ← Important!

This is a great way to save tax even in the new regime — ask HR to structure employer NPS contribution.

## Total Maximum NPS Deduction

| Section | Limit |
|---|---|
| 80CCD(1) within 80C | ₹1,50,000 |
| 80CCD(1B) extra | ₹50,000 |
| 80CCD(2) employer | 10–14% of salary |

## Example: ₹20L Salary, Old Regime

Employer NPS contribution: 10% of ₹9L basic = ₹90,000
Employee NPS 80CCD(1B): ₹50,000

Total NPS deduction:
- 80C (includes 80CCD(1)): ₹1,50,000
- 80CCD(1B): ₹50,000
- 80CCD(2): ₹90,000
- **Total NPS benefit: ₹2,90,000**

Tax saved (30% bracket): ~₹90,480

## NPS Returns & Withdrawal

- Returns: Market-linked (equity + bonds mix) — typically 9–11% long term
- At 60: 60% lump sum (tax-free), 40% mandatory annuity (taxable)
- Partial withdrawal: allowed after 3 years for specific purposes
''',
    },
    {
        'title': 'Which ITR Form Should You File? Complete Guide',
        'slug': 'which-itr-form-should-you-file-complete-guide',
        'category': 'income-tax',
        'tags': 'ITR form,ITR-1,ITR-2,ITR-3,ITR-4,which ITR to file',
        'excerpt': 'ITR-1, ITR-2, ITR-3, or ITR-4? This guide tells you exactly which form to use based on your income sources, with a decision flowchart.',
        'meta_title': 'Which ITR Form to File? ITR-1 vs ITR-2 vs ITR-3 vs ITR-4',
        'meta_description': 'Which ITR form to file for AY 2026-27? Decision guide for ITR-1 (salaried), ITR-2 (capital gains), ITR-3 (business), ITR-4 (presumptive). Simple flowchart.',
        'reading_time': 6,
        'body': '''## Which ITR Form to File? — AY 2026-27

Choosing the wrong ITR form means defective return notice. Here's the definitive guide.

## ITR-1 (Sahaj) — Simplest Form

**Use if you have:**
- Salary income only (any amount)
- One house property (no losses)
- Other income: interest, dividends
- Income < ₹50 lakh total
- No capital gains
- No foreign assets or income

**Cannot use if:**
- Director in a company
- Have ESOPs
- Agricultural income > ₹5,000

**Most salaried employees file ITR-1.**

## ITR-2 — For Multiple Income Sources

**Use if you have:**
- Capital gains (stocks, mutual funds, property)
- More than one house property
- Foreign income or assets
- Income > ₹50 lakh
- Agricultural income > ₹5,000
- Director in a company (no business income)

## ITR-3 — Business/Profession (Actual Books)

**Use if you have:**
- Business income with actual books of accounts
- Partnership firm share
- Freelance income where you maintain full accounts
- F&O trading income (always business income)

## ITR-4 (Sugam) — Presumptive Taxation

**Use if you have:**
- Business under **Section 44AD** (turnover ≤ ₹3Cr)
- Professional income under **Section 44ADA** (receipts ≤ ₹75L)
- Transport business under **44AE**
- Also salary + interest income allowed

**Cannot use if:**
- Income > ₹50 lakh
- Have foreign assets
- Have carry-forward losses

## Quick Flowchart

```
Salaried only, no cap gains, income < ₹50L? → ITR-1
Salaried + capital gains? → ITR-2
Freelancer/consultant (44ADA)? → ITR-4
F&O trading? → ITR-3
Business with books? → ITR-3
Multiple incomes, complex? → ITR-2 or ITR-3
```

## Deadline — AY 2026-27

| Category | Due Date |
|---|---|
| Individuals (no audit) | July 31, 2026 |
| Audit cases | October 31, 2026 |
| Transfer pricing | November 30, 2026 |

Late filing: ₹5,000 fee (₹1,000 if income < ₹5L)
''',
    },
    {
        'title': 'How to Save Tax on Salary Above ₹10 Lakhs in India',
        'slug': 'how-to-save-tax-salary-above-10-lakhs-india',
        'category': 'income-tax',
        'tags': 'tax saving,salary,10 lakh,deductions,80C,HRA,NPS,home loan',
        'excerpt': 'Salary above ₹10L? Here are the best tax-saving strategies combining HRA, 80C, NPS, 80D, and home loan benefits to reduce your tax bill legally.',
        'meta_title': 'How to Save Tax on Salary Above ₹10 Lakhs: 8 Strategies',
        'meta_description': 'Save tax on salary above ₹10 lakhs. Combine HRA, 80C (₹1.5L), NPS extra (₹50K), 80D (₹25K), home loan to reduce taxable income by ₹5L+.',
        'reading_time': 8,
        'body': '''## Tax on ₹10L+ Salary — And How to Reduce It

At ₹10L salary (new regime), you'd pay ~₹54,600 tax. In old regime with max deductions, you can bring it to near zero.

## Maximum Deductions Available (Old Regime)

| Deduction | Maximum |
|---|---|
| Standard Deduction | ₹50,000 |
| HRA Exemption | Up to ₹2,00,000+ |
| Section 80C | ₹1,50,000 |
| NPS Extra (80CCD(1B)) | ₹50,000 |
| Health Insurance (80D) | ₹25,000 |
| Home Loan Interest (24b) | ₹2,00,000 |
| **Total Possible** | **₹6,75,000+** |

At ₹10L gross income: ₹10L – ₹6.75L = ₹3.25L taxable → near zero tax!

## Strategy 1: Maximise 80C (₹1.5L)

Priority order:
1. EPF mandatory contribution (auto, counts toward 80C)
2. ELSS mutual fund (remaining amount)
3. PPF if you want guaranteed returns

Don't buy ULIP just to fill 80C — poor returns, high charges.

## Strategy 2: NPS Extra Deduction (₹50,000 Free)

Open NPS Tier 1 account → contribute ₹50,000/year → get deduction under 80CCD(1B).

This is separate from 80C limit. Pure additional tax saving.

## Strategy 3: HRA — Maximise Rent

If you're in a rented house, ensure full HRA exemption:
- Submit rent receipts to employer
- If rent > ₹8,333/month (₹1L/year), provide landlord's PAN
- Metro city? Claim 50% of basic

If living in own house or parents' house: consider old regime may not benefit.

## Strategy 4: Health Insurance (80D)

- Buy health insurance for self + family: ₹20–25K/year → deduction up to ₹25K
- Add parents' policy (senior citizen): ₹42–50K → deduction up to ₹50K
- Combined: ₹75,000 deduction

## Strategy 5: Home Loan

Taking a home loan? Claim:
- ₹2L interest (Section 24) + ₹1.5L principal (within 80C)
- Consider joint loan with spouse for double deduction

## Strategy 6: Employer Benefits

Talk to HR about:
- **NPS employer contribution (80CCD(2))**: Available even in new regime!
- Sodexo/meal vouchers: ₹2,200/month tax-free
- Leave Travel Allowance (LTA): 2 journeys in 4-year block tax-free

## New Regime vs Old Regime at ₹10L

| Deductions | Old Regime Tax | New Regime Tax |
|---|---|---|
| Zero deductions | ₹54,600 | ₹54,600 |
| ₹3L deductions | ~₹16,000 | ₹54,600 |
| ₹5L+ deductions | ~₹0 | ₹54,600 |

With high deductions, **old regime wins** above ₹10L.

Use the [Old vs New Regime Calculator](/tools/old-vs-new-tax-regime/) to find your winner.
''',
    },
]

CATEGORIES = {
    'income-tax': {'name': 'Income Tax', 'description': 'Income tax slabs, regime comparison, TDS, ITR filing guides'},
    'deductions': {'name': 'Deductions & Savings', 'description': '80C, 80D, HRA, NPS, home loan tax benefits'},
    'gst': {'name': 'GST', 'description': 'GST rates, registration, filing, ITC, composition scheme'},
    'investments': {'name': 'Investments & Capital Gains', 'description': 'Mutual funds, stocks, capital gains tax, ELSS, PPF'},
    'freelancer': {'name': 'Freelancer & Business', 'description': 'Presumptive tax, 44ADA, 44AD, business income tax'},
}

AUTHOR = {
    'name': 'Priya Sharma',
    'title': 'Chartered Accountant (CA) — 12 Years Experience',
    'bio': (
        'Priya Sharma is a Chartered Accountant with 12 years of experience in Indian '
        'income tax, GST, and financial planning. She has helped over 500 clients optimise '
        'their tax savings and is a regular contributor to financial publications.'
    ),
    'is_ca': True,
}


class Command(BaseCommand):
    help = 'Seed blog with categories, author, and 15 articles'

    def handle(self, *args, **options):
        self.stdout.write('Seeding blog...')

        # Categories
        cats = {}
        for slug, data in CATEGORIES.items():
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': data['name'], 'description': data['description']},
            )
            cats[slug] = cat
            self.stdout.write(f'  Category: {cat.name} ({"created" if created else "exists"})')

        # Author
        author, created = Author.objects.get_or_create(
            name=AUTHOR['name'],
            defaults={
                'title': AUTHOR['title'],
                'bio': AUTHOR['bio'],
                'is_ca': AUTHOR['is_ca'],
            },
        )
        self.stdout.write(f'  Author: {author.name} ({"created" if created else "exists"})')

        # Articles
        for i, art in enumerate(ARTICLES, 1):
            cat_slug = art.get('category', 'income-tax')
            category = cats.get(cat_slug)
            tool_slug = art.pop('tool_slug', None)
            category_key = art.pop('category')

            obj, created = Article.objects.get_or_create(
                slug=art['slug'],
                defaults={
                    'title': art['title'],
                    'author': author,
                    'category': category,
                    'tags': art.get('tags', ''),
                    'body': art['body'],
                    'excerpt': art['excerpt'],
                    'meta_title': art['meta_title'],
                    'meta_description': art['meta_description'],
                    'reading_time': art.get('reading_time', 6),
                    'is_featured': art.get('is_featured', False),
                    'is_published': True,
                    'published_at': timezone.now(),
                    'fy_applicable': '2025-26',
                },
            )

            if created and tool_slug:
                try:
                    tool = Tool.objects.get(slug=tool_slug)
                    obj.related_tools.add(tool)
                except Tool.DoesNotExist:
                    pass

            self.stdout.write(
                f'  [{i:02d}] {obj.title[:60]} ({"created" if created else "exists"})'
            )

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {Article.objects.count()} articles, '
            f'{Author.objects.count()} authors, '
            f'{Category.objects.count()} categories.'
        ))
