"""
Seed extra US blog articles — 10 more high-traffic topics.
Run: python manage.py seed_us_blog_extra
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import Article, Author, Category


ARTICLES = [
    {
        'slug': 'w2-vs-1099-tax-differences-2025',
        'title': 'W-2 vs 1099: Tax Differences, Pros and Cons in 2025',
        'category': 'us-self-employment',
        'market': 'us',
        'fy_applicable': '2025',
        'is_featured': True,
        'reading_time': 9,
        'tags': 'W-2 vs 1099, employee vs contractor, 1099 taxes, self employment',
        'excerpt': 'W-2 employee or 1099 contractor? The tax difference is huge. 1099 workers pay 15.3% SE tax plus income tax, but get more deductions. Here is how it compares.',
        'meta_title': 'W-2 vs 1099: Tax Differences Explained for 2025',
        'meta_description': 'W-2 vs 1099 tax comparison for 2025. SE tax on 1099, FICA on W-2, deductions available to each. With calculator and examples.',
        'body': '''## W-2 vs 1099: What Is the Tax Difference?

The classification of your work — employee (W-2) or independent contractor (1099) — has massive tax implications.

## How W-2 Employees Are Taxed

As a W-2 employee:
- Your employer withholds **federal income tax**, **Social Security (6.2%)**, and **Medicare (1.45%)** from your paycheck
- Your employer pays the **other half** of FICA taxes (6.2% SS + 1.45% Medicare)
- You receive a **W-2 form** in January showing all withholding
- Most deductions require itemizing (harder to qualify)

**Effective FICA burden:** You pay 7.65%, employer pays 7.65% = total 15.3%

## How 1099 Contractors Are Taxed

As a 1099 contractor (self-employed):
- **No withholding** — you receive full payment, pay taxes yourself
- You pay **self-employment tax** = 15.3% of 92.35% of net profit
- You pay this ON TOP of regular income tax
- You must pay **quarterly estimated taxes** (April, June, September, January)
- You get MORE deductions: home office, equipment, health insurance, retirement

## Side-by-Side Comparison

| | W-2 Employee | 1099 Contractor |
|---|---|---|
| FICA taxes | 7.65% (you) + 7.65% (employer) | 15.3% (you pay all) |
| Withholding | Automatic | None — you pay quarterly |
| Deductions | Limited (standard deduction) | Business expenses deductible |
| Health insurance | Pre-tax through employer | 100% deductible (self-employed) |
| Retirement | 401(k) match possible | Solo 401(k) / SEP-IRA (higher limits) |
| Unemployment benefits | Eligible | Not eligible |
| Workers comp | Covered | Not covered |

## Example: $80,000 Income

**W-2 Employee at $80,000:**
- FICA you pay: $6,120 (7.65%)
- Federal income tax: ~$7,648 (single, standard deduction)
- Total tax: ~$13,768
- Take-home: ~$66,232

**1099 Contractor at $80,000 net profit:**
- SE tax: $11,304 (15.3% × 92.35% × $80K)
- SE deduction (half): -$5,652
- Federal income tax on $74,348: ~$10,144
- Total tax: ~$21,448
- Take-home: ~$58,552

**The 1099 gap: ~$7,680 more in taxes** — but you can close this with deductions.

## 1099 Deductions That Reduce the Gap

| Deduction | Saves (30% bracket) |
|---|---|
| Home office (300 sqft × $5/sqft = $1,500) | $450 |
| Internet ($100/mo = $1,200/yr) | $360 |
| Laptop ($1,500) | $450 |
| Health insurance premium ($6,000/yr) | $1,800 |
| SEP-IRA contribution ($10,000) | $3,000 |
| **Total saved** | **$6,060** |

With smart deductions, the 1099 tax gap shrinks significantly.

## Should You Ask to Be 1099?

Ask to be 1099 if:
- Your effective deductions + SE deduction offset the SE tax
- You value flexibility and higher retirement contribution limits (SEP-IRA up to $69,000/year)
- Your marginal rate makes the deductions valuable

Stay W-2 if:
- Your employer provides valuable benefits (401k match, health insurance)
- You want simplicity
- You have no significant business expenses

Use our [Self-Employment Tax Calculator](/tools/us-self-employment-tax-calculator/) to see your exact numbers.
''',
    },
    {
        'slug': 'child-tax-credit-2025-guide',
        'title': 'Child Tax Credit 2025: How Much, Who Qualifies, How to Claim',
        'category': 'us-income-tax',
        'market': 'us',
        'fy_applicable': '2025',
        'is_featured': True,
        'reading_time': 7,
        'tags': 'child tax credit 2025, CTC, dependent credit, refundable credit',
        'excerpt': 'The Child Tax Credit in 2025 is worth up to $2,000 per qualifying child, with up to $1,700 refundable. Here is who qualifies, income phaseouts, and how to claim it on your return.',
        'meta_title': 'Child Tax Credit 2025: Amount, Income Limits & How to Claim',
        'meta_description': 'Child Tax Credit 2025: $2,000 per child, $1,700 refundable ACTC, income phaseout at $200K single / $400K married. How to claim on Form 8812.',
        'body': '''## Child Tax Credit 2025

The Child Tax Credit (CTC) is one of the most valuable credits on a US tax return — worth up to $2,000 per qualifying child.

## How Much Is the Credit?

| Credit | Amount Per Child |
|---|---|
| Child Tax Credit | Up to **$2,000** |
| Additional Child Tax Credit (refundable) | Up to **$1,700** |

The $1,700 ACTC portion is **refundable** — meaning you can get it even if you owe no tax.

## Who Qualifies?

Your child must:
- Be under **17** at the end of the tax year (December 31, 2025)
- Have a valid **Social Security Number**
- Be your dependent (child, stepchild, foster child, sibling, etc.)
- Live with you for more than half the year
- Not provide more than half of their own support

## Income Phaseout Limits

The credit reduces by $50 for every $1,000 (or fraction) above:

| Filing Status | Phaseout Begins | Credit Fully Gone |
|---|---|---|
| Single / MFS | $200,000 | $240,000 |
| Married Filing Jointly | $400,000 | $440,000 |

**Example:** Married couple, $410,000 income, 2 children:
- Income over threshold: $10,000
- Reduction: 10 × $50 = $500 per child
- Credit: ($2,000 - $500) × 2 = $3,000

## Additional Child Tax Credit (ACTC)

The ACTC is refundable — if the CTC exceeds your tax liability, you can get a refund.

ACTC = 15% of earned income exceeding **$2,500**, up to $1,700 per child.

**Example:** Single parent, 1 child, $25,000 earned income, $0 tax liability:
- ACTC = 15% × ($25,000 - $2,500) = 15% × $22,500 = $3,375, capped at $1,700
- **Refund from ACTC: $1,700**

## How to Claim

1. Complete **Schedule 8812** (Credits for Qualifying Children)
2. Enter credit on **Form 1040, Line 19**
3. ACTC goes to **Line 28**

## Other Dependent Credit

For dependents who do NOT qualify for CTC (age 17+, parents, etc.):
- **$500 non-refundable** Other Dependent Credit
- Same income phaseout as CTC

## Common Mistakes

- Claiming a child who is 17+ (must be UNDER 17 on Dec 31)
- Forgetting to include child's SSN
- Not claiming ACTC when you get a small refund or owe little

Use our [Federal Income Tax Calculator](/tools/us-federal-income-tax-calculator/) — it factors in CTC automatically.
''',
    },
    {
        'slug': 'tax-deductions-homeowners-2025',
        'title': 'Tax Deductions for Homeowners in 2025: Everything You Can Deduct',
        'category': 'us-income-tax',
        'market': 'us',
        'fy_applicable': '2025',
        'reading_time': 8,
        'tags': 'homeowner tax deductions, mortgage interest deduction, property tax deduction, SALT',
        'excerpt': 'Own a home? You may qualify for the mortgage interest deduction, property tax deduction, home office deduction, and more. Here is everything homeowners can deduct in 2025.',
        'meta_title': 'Homeowner Tax Deductions 2025: Mortgage, Property Tax & More',
        'meta_description': 'Tax deductions for homeowners 2025: mortgage interest (up to $750K loan), property tax (SALT cap $10K), home office, energy credits. Full guide.',
        'body': '''## Tax Deductions for Homeowners 2025

Owning a home unlocks several valuable tax deductions — but you need to **itemize** to claim most of them. Here is what is available.

## 1. Mortgage Interest Deduction

Deduct interest paid on your mortgage if:
- Loan balance ≤ **$750,000** (for loans after Dec 15, 2017)
- Loans before that date: up to **$1,000,000** grandfathered
- Property is your primary or secondary home

**Example:** $500,000 mortgage at 7% = $35,000 interest in year 1. If you itemize, deduct $35,000 from taxable income.

**Tax saved (24% bracket):** $35,000 × 24% = **$8,400**

Points paid to get a lower mortgage rate: generally deductible in full in the year paid for a primary home purchase.

## 2. Property Tax Deduction (SALT Cap)

State and local taxes — including property taxes — are deductible, but capped at **$10,000 per year** (SALT limit).

The $10,000 cap covers:
- State income taxes OR state sales taxes (pick one)
- Property taxes on any number of properties

If you pay $8,000 property tax + $5,000 state income tax = $13,000 total, you can only deduct **$10,000**.

## 3. Home Office Deduction (Self-Employed Only)

If you work from home and are **self-employed** (not W-2), you can deduct:

**Simplified method:** $5 per square foot, up to 300 sq ft = max **$1,500/year**

**Regular method:** Actual expenses × (office sq ft ÷ total home sq ft)
- Mortgage interest portion
- Utilities portion
- Repairs portion
- Depreciation

W-2 employees: home office deduction **not available** since 2018 tax reform.

## 4. Mortgage Insurance Premium (PMI)

If you put less than 20% down, you pay Private Mortgage Insurance.
- PMI was deductible through 2021 — **currently expired for 2025** unless Congress extends it.
- Check IRS.gov for current status.

## 5. Energy Efficiency Credits

These are **credits** (better than deductions — dollar-for-dollar reduction in tax):

| Improvement | Credit | Cap |
|---|---|---|
| Solar panels (Sec 25D) | 30% of cost | None |
| Energy-efficient windows/doors | 30% of cost | $600/item |
| Heat pump / HVAC | 30% of cost | $2,000 |
| Insulation | 30% of cost | $1,200 |

Example: $20,000 solar installation → **$6,000 tax credit**

## 6. Capital Gains Exclusion on Sale

This is not a deduction — it is better. When you sell your primary home:
- Single: **$250,000** of profit tax-free
- Married: **$500,000** of profit tax-free

Requirements:
- Owned for at least 2 of last 5 years
- Used as primary residence for at least 2 of last 5 years

## Itemizing vs. Standard Deduction

You only benefit from these deductions if they exceed the standard deduction:

| Status | 2025 Standard Deduction |
|---|---|
| Single | $15,000 |
| Married Filing Jointly | $30,000 |

**Example:** Mortgage interest $12,000 + property tax $8,000 = $20,000 itemized.
- Single: $20,000 > $15,000 → itemize saves more
- Married: $20,000 < $30,000 → standard deduction is better

Use our [Standard vs. Itemized Deduction Calculator](/tools/us-standard-vs-itemized-deduction/) to see which is better for you.
''',
    },
    {
        'slug': 'roth-ira-vs-traditional-ira-2025',
        'title': 'Roth IRA vs Traditional IRA: Which Is Better for You in 2025?',
        'category': 'us-investments',
        'market': 'us',
        'fy_applicable': '2025',
        'reading_time': 9,
        'tags': 'Roth IRA, Traditional IRA, IRA comparison, retirement savings, tax-free growth',
        'excerpt': 'Roth or Traditional IRA? The key difference is when you pay tax — now (Roth) or later (Traditional). Here is exactly how to choose based on your tax rate today vs. in retirement.',
        'meta_title': 'Roth IRA vs Traditional IRA 2025: Which Is Better?',
        'meta_description': 'Roth IRA vs Traditional IRA for 2025. $7,000 contribution limit ($8,000 if 50+). When to choose Roth, when Traditional wins, income limits explained.',
        'body': '''## Roth IRA vs Traditional IRA — 2025 Guide

Both IRAs are powerful retirement accounts, but they are taxed differently. The right choice depends on whether you expect to be in a higher or lower tax bracket in retirement.

## 2025 Contribution Limits

| Account | Limit | 50+ Catch-up |
|---|---|---|
| Roth IRA | $7,000 | $8,000 |
| Traditional IRA | $7,000 | $8,000 |

You can split contributions across both, but the total cannot exceed $7,000 ($8,000 if 50+).

## Key Difference: When You Pay Tax

**Traditional IRA:**
- Contribute **pre-tax** (deductible from current income)
- Grows tax-deferred
- Withdrawals in retirement = **taxable income**
- Required Minimum Distributions (RMDs) start at age 73

**Roth IRA:**
- Contribute **after-tax** (no deduction now)
- Grows **tax-free**
- Qualified withdrawals in retirement = **completely tax-free**
- No RMDs during your lifetime

## Income Limits (2025)

### Roth IRA Contribution Limits

| Filing Status | Full Contribution | Phase-out | No Contribution |
|---|---|---|---|
| Single | Under $150,000 | $150K–$165K | Above $165,000 |
| Married Filing Jointly | Under $236,000 | $236K–$246K | Above $246,000 |

### Traditional IRA Deductibility (if covered by workplace plan)

| Filing Status | Full Deduction | Phase-out | No Deduction |
|---|---|---|---|
| Single | Under $79,000 | $79K–$89K | Above $89,000 |
| Married | Under $126,000 | $126K–$146K | Above $146,000 |

No income limit if NOT covered by a workplace plan.

## Choose Roth If...

- You are in a **low tax bracket now** (e.g., 10–22%) but expect to be higher in retirement
- You are young with decades of tax-free growth ahead
- You want **flexibility** — contributions (not earnings) can be withdrawn anytime, no penalty
- You want to leave tax-free money to heirs
- Your income is below the Roth limit

## Choose Traditional If...

- You are in a **high tax bracket now** (24–37%) and expect to be lower in retirement
- You need the deduction to lower taxable income this year
- You are closer to retirement with fewer years of growth
- Your income exceeds Roth limits (but consider Backdoor Roth)

## Backdoor Roth — For High Earners

If your income exceeds Roth limits:
1. Contribute $7,000 to a **non-deductible Traditional IRA**
2. Convert it to Roth immediately (no tax if no other Traditional IRA balance)

This strategy lets high earners access Roth benefits. Consult a tax advisor if you have existing Traditional IRA balances (pro-rata rule applies).

## Example: $7,000 Investment Over 30 Years (7% growth)

|  | Roth IRA | Traditional IRA |
|---|---|---|
| Contribution | $7,000 after-tax | $7,000 pre-tax ($5,040 real cost at 28%) |
| Value at 30 years | $53,322 | $53,322 |
| Tax on withdrawal (28%) | $0 | $14,930 |
| **After-tax value** | **$53,322** | **$38,392** |

Roth wins if your tax rate stays the same or rises. Traditional wins if rate drops significantly.

## The Simple Rule

- **In 10–22% bracket:** Roth
- **In 24–32% bracket:** Depends — compare current vs. expected retirement rate
- **In 35–37% bracket:** Traditional (get the deduction now)
''',
    },
    {
        'slug': 'irs-payment-plan-installment-agreement-2025',
        'title': 'IRS Payment Plan 2025: How to Set Up an Installment Agreement',
        'category': 'us-tax-guides',
        'market': 'us',
        'fy_applicable': '2025',
        'reading_time': 7,
        'tags': 'IRS payment plan, installment agreement, IRS debt, can not pay taxes',
        'excerpt': 'Cannot pay your tax bill in full? The IRS offers payment plans — monthly installments, Offer in Compromise, and Currently Not Collectible status. Here is how to apply.',
        'meta_title': 'IRS Payment Plan 2025: Set Up Installment Agreement Online',
        'meta_description': 'Cannot pay IRS tax debt? Set up an installment agreement online. Short-term (120 days free) and long-term plans. Interest still accrues. 2025 guide.',
        'body': '''## IRS Payment Plan — Options for 2025

If you cannot pay your tax bill in full, the IRS offers several options. Ignoring the debt is the worst choice — interest and penalties compound quickly.

## Option 1: Short-Term Payment Plan (Free)

- Pay in full within **120 days**
- No setup fee
- Interest (currently ~8% per year) and late-payment penalty still accrue
- Apply online at IRS.gov → Online Payment Agreement tool

**Best for:** You can pay in full in a few months but need time.

## Option 2: Long-Term Installment Agreement

**Online installment agreement** (IRS.gov — fastest):

| Balance Owed | Setup Fee | With Direct Debit |
|---|---|---|
| Any amount | $31 | $31 (direct debit) |
| Any amount | $130 | $107 (non-direct debit) |
| Low income (under 250% poverty) | $43 | $0 if direct debit |

**By phone or mail:** Higher fees — use online when possible.

**Terms:**
- Must pay off within 72 months (6 years) OR before the Collection Statute Expiration Date
- Continue to file all future returns on time
- Interest (~8%/year) and failure-to-pay penalty (0.25%/month on installment plan) continue to accrue

## Option 3: Offer in Compromise (OIC)

Settle for less than the full amount you owe if:
- You cannot pay the full balance within the remaining collection period
- Paying in full would cause "economic hardship"

**Application fee:** $205 (waived for low-income applicants)

OIC acceptance rate is low (~40%). The IRS evaluates your ability to pay based on income, expenses, and asset equity. Many paid "tax relief" companies promise OIC but deliver nothing — be skeptical.

## Option 4: Currently Not Collectible (CNC)

If you truly cannot afford to pay anything — no income, no assets:
- IRS pauses collection activity
- Debt does not go away — it sits and accrues interest
- IRS reviews your situation periodically

## Penalties While on a Payment Plan

| Penalty | Rate |
|---|---|
| Late-payment penalty | 0.5%/month (reduced to 0.25% on installment plan) |
| Failure-to-file penalty | 5%/month (up to 25%) — always file on time! |
| Interest | Federal short-term rate + 3% (~8% in 2025) |

**Critical:** Always file your return on time even if you cannot pay. The failure-to-file penalty (5%/month) is 10x worse than the failure-to-pay penalty (0.5%/month).

## How to Apply Online (Step by Step)

1. Go to **IRS.gov** → "Pay" → "Payment Plan"
2. Log in or create an IRS Online Account
3. Select: "Individual installment agreement"
4. Enter proposed monthly payment
5. Choose direct debit (lowest fee, automatic payments)
6. Accept terms → IRS approves most online requests immediately

## What to Do If the IRS Is Already Collecting

If you have received:
- **CP2000 notice** (proposed changes) → respond within 60 days
- **CP503/504 notice** (balance due reminder) → set up payment plan immediately
- **Final Notice (LT11/Letter 1058)** → 30 days before levy — act NOW
- **Bank levy or wage garnishment** → call IRS immediately at 1-800-829-1040

The IRS will stop collection action once you are on an approved payment plan.

## State Taxes

Most states offer similar installment agreements. Contact your state's Department of Revenue. State and federal agreements are separate.
''',
    },
    {
        'slug': 'social-security-tax-guide-2025',
        'title': 'Social Security Tax 2025: What You Pay, When It Stops, and Benefits',
        'category': 'us-income-tax',
        'market': 'us',
        'fy_applicable': '2025',
        'reading_time': 7,
        'tags': 'social security tax, FICA, OASDI, wage base limit, Social Security benefits tax',
        'excerpt': 'Social Security tax in 2025 is 6.2% on wages up to $176,100. Here is how it works for employees, self-employed, and retirees — including when your SS benefits become taxable.',
        'meta_title': 'Social Security Tax 2025: Rate, Wage Base, How It Works',
        'meta_description': 'Social Security tax 2025: 6.2% employee rate, 12.4% self-employed. $176,100 wage base. When SS benefits are taxable. Full FICA breakdown.',
        'body': '''## Social Security Tax — 2025 Guide

Social Security (OASDI) tax funds the Social Security program. Here is everything you need to know.

## 2025 Tax Rate and Wage Base

| | Employee | Employer | Self-Employed |
|---|---|---|---|
| Social Security rate | 6.2% | 6.2% | 12.4% |
| Medicare rate | 1.45% | 1.45% | 2.9% |
| **Total FICA** | **7.65%** | **7.65%** | **15.3%** |
| Wage base (SS only) | $176,100 | $176,100 | $176,100 |
| Medicare wage base | No limit | No limit | No limit |

**Maximum SS tax (employee):** $176,100 × 6.2% = **$10,918.20**

Once you earn above $176,100 in a calendar year, SS tax stops. Medicare tax continues on all earnings.

## Additional Medicare Tax (High Earners)

If income exceeds:
- $200,000 (single)
- $250,000 (married filing jointly)

An additional **0.9% Medicare tax** applies to earnings above these thresholds. Employers do not match this.

## Self-Employed — SE Tax

Self-employed workers pay both sides (12.4% SS + 2.9% Medicare = 15.3%).

However:
- SE tax applies to **92.35%** of net profit (equivalent to the employee's share)
- You deduct **half of SE tax** from gross income (not a credit — a deduction)

**Example:** $100,000 net profit
- SE tax base: $92,350
- SE tax: $14,130
- Deduction: $7,065 (half of SE tax)
- Reduces your income tax and increases take-home

## Multiple Jobs — Watch for Overwithholding

If you have two W-2 jobs and combined wages exceed $176,100:
- Each employer withholds SS up to their $176,100 limit
- You may end up **over-withheld** for SS tax
- Claim the excess as a **refundable credit** on Form 1040 (Schedule 3, Line 11)

## Are Social Security Benefits Taxable?

If you collect Social Security benefits, part may be taxable based on your "combined income":

**Combined income** = Adjusted Gross Income + non-taxable interest + 50% of SS benefits

| Combined Income | Benefits Taxable |
|---|---|
| Single under $25,000 | 0% taxable |
| Single $25,000–$34,000 | Up to 50% taxable |
| Single above $34,000 | Up to 85% taxable |
| Married under $32,000 | 0% taxable |
| Married $32,000–$44,000 | Up to 50% taxable |
| Married above $44,000 | Up to 85% taxable |

**Maximum:** 85% of SS benefits can be taxable — never 100%.

**Tip:** Manage IRA withdrawals and income sources in retirement to minimize combined income and keep more SS benefits tax-free.

## When Does SS Tax Benefit You?

Every dollar of SS tax you pay earns you credits toward future SS benefits. You need **40 credits** (10 years of work) to qualify for retirement benefits.

The more you earn and pay in (up to the wage base), the higher your eventual monthly benefit.

## SE Tax Deduction — Example

$80,000 net freelance profit:
- SE tax: $11,304 (15.3% × 92.35% × $80K)
- SE deduction: $5,652 (half of SE tax)
- Reduces AGI by $5,652 → saves ~$1,356 in income tax (24% bracket)

Use our [Self-Employment Tax Calculator](/tools/us-self-employment-tax-calculator/) to see your exact SE tax, deduction, and take-home.
''',
    },
    {
        'slug': 'tax-loss-harvesting-guide-2025',
        'title': 'Tax-Loss Harvesting 2025: How to Cut Your Investment Tax Bill',
        'category': 'us-investments',
        'market': 'us',
        'fy_applicable': '2025',
        'reading_time': 8,
        'tags': 'tax loss harvesting, capital gains offset, wash sale rule, investment tax strategy',
        'excerpt': 'Tax-loss harvesting lets you sell losing investments to offset capital gains and up to $3,000 of ordinary income. Here is how it works, the wash-sale rule, and when to use it.',
        'meta_title': 'Tax-Loss Harvesting 2025: Strategy, Wash-Sale Rule & Examples',
        'meta_description': 'Tax-loss harvesting 2025: offset capital gains with losses, deduct $3,000 against ordinary income, carry forward unlimited losses. Wash-sale rule explained.',
        'body': '''## Tax-Loss Harvesting — 2025 Guide

Tax-loss harvesting is the practice of selling investments at a loss to offset capital gains — reducing your tax bill without fundamentally changing your investment strategy.

## How It Works

1. You have $10,000 in capital gains from selling Stock A
2. You also hold Stock B, currently down $7,000
3. Sell Stock B — realize the $7,000 loss
4. Net taxable gain: $10,000 - $7,000 = **$3,000** (instead of $10,000)
5. Tax saved (15% LTCG rate): $7,000 × 15% = **$1,050**

## Gain-Loss Netting Rules

The IRS requires specific ordering:
1. Short-term losses offset short-term gains first
2. Long-term losses offset long-term gains first
3. Remaining losses cross-offset (ST losses vs LT gains, etc.)

**Net short-term gains** are taxed as ordinary income (up to 37%).
**Net long-term gains** get preferential rates (0%, 15%, or 20%).

## The $3,000 Ordinary Income Deduction

If total capital losses exceed total capital gains, you can deduct up to **$3,000** against ordinary income per year.

**Example:** $15,000 in losses, $5,000 in gains:
- Net loss: $10,000
- Year 1: Deduct $3,000 from ordinary income → saves $720 (24% bracket)
- Carry forward $7,000 → deduct in future years

**Losses carry forward indefinitely** until fully used.

## The Wash-Sale Rule — Critical

You **cannot** buy the same or "substantially identical" security within **30 days before or after** the sale.

If you violate the wash-sale rule:
- The loss is **disallowed** for that year
- The disallowed loss is added to your cost basis of the replacement shares
- You do not permanently lose the loss — it is deferred

**30-day window:** 61 total days (30 days before + sale day + 30 days after)

### What Counts as "Substantially Identical"?

- Selling and buying the **same stock**: Wash sale
- Selling SPY (S&P 500 ETF) and buying VOO (S&P 500 ETF): Likely wash sale
- Selling SPY and buying VTI (Total Market ETF): Generally NOT a wash sale
- Selling a mutual fund and buying a similar but different fund: Generally OK
- Stock options of the same company: Watch sale with the stock

## Strategies to Harvest Without Wash-Sale Issues

**Strategy 1 — Wait 31 days:**
- Sell at a loss
- Buy a similar (not substantially identical) fund immediately to maintain market exposure
- After 31 days, sell the replacement and buy back the original

**Strategy 2 — Similar fund swap:**
- Sell iShares S&P 500 ETF (IVV)
- Immediately buy Vanguard S&P 500 ETF (VOO) — different provider, same index
- After 31 days, optional swap back

(Note: The IRS has not ruled specifically on ETF swaps — this is a gray area. Consult a tax advisor.)

## When to Harvest Losses

**Harvest in:** December (most common), but also during market drops throughout the year.

**Best candidates for harvesting:**
- Individual stocks in taxable accounts with unrealized losses
- Sector ETFs that have underperformed
- Any holding down >5% with an offsetting gain somewhere else

**Do not harvest in:** Tax-advantaged accounts (IRA, 401k) — no capital gains in those accounts anyway.

## Tax-Loss Harvesting vs. Holding

**Important:** Harvesting defers taxes, it does not eliminate them. Your replacement shares have a lower cost basis — future gains will be higher.

It is most beneficial when:
- You have offsetting gains to eliminate
- You are in a high capital gains tax bracket (20% + NIIT)
- You can reinvest for years and let compounding work on the saved tax amount

Use our [Capital Gains Tax Calculator](/tools/us-capital-gains-tax-calculator/) to see the tax impact of your gains and losses.
''',
    },
    {
        'slug': 'how-to-file-taxes-free-2025',
        'title': 'How to File Your Taxes for Free in 2025 (IRS Free File, Direct File)',
        'category': 'us-tax-guides',
        'market': 'us',
        'fy_applicable': '2025',
        'reading_time': 6,
        'tags': 'free tax filing 2025, IRS Free File, IRS Direct File, free tax software',
        'excerpt': 'Most Americans can file their federal taxes for free in 2025 using IRS Free File, IRS Direct File, or free editions of major tax software. Here is which option is right for you.',
        'meta_title': 'How to File Taxes Free in 2025: IRS Free File & Direct File',
        'meta_description': 'File federal taxes free in 2025. IRS Free File (AGI under $84,000), IRS Direct File (simple returns), FreeTaxUSA, Cash App Taxes. Full comparison.',
        'body': '''## How to File Taxes for Free in 2025

The IRS offers multiple truly free filing options. You do not need to pay $50–$150 to a tax software company if your return is not complex.

## Option 1: IRS Free File (Most People Qualify)

**Who qualifies:** AGI (adjusted gross income) of **$84,000 or less** in 2025

**How it works:**
- Go to IRS.gov/freefile
- Choose from 8 partner software companies
- File federal taxes completely free
- Many partners also offer free state filing

**Partners include:** TaxAct, TaxSlayer, FreeTaxUSA, and others
Each partner has slightly different eligibility requirements (age limits, state restrictions). Use the IRS lookup tool to find the best match.

## Option 2: IRS Direct File (Simple Returns)

**New for 2024/2025** — IRS's own free filing software.

**Available in:** All 50 states for 2025

**Best for:**
- W-2 income only
- Standard deduction
- Common credits: CTC, EITC, student loan interest
- Limited investment income

**Not available for:**
- Self-employment income
- Rental income
- Complex investments
- Itemized deductions

Go to directfile.irs.gov to see if your situation qualifies.

## Option 3: Free Editions of Major Software

### FreeTaxUSA — Best Free Option for Most
- **Federal:** Completely free for all returns
- **State:** $14.99 per state
- Handles: self-employment, investments, rental income, all schedules
- Highly rated, no income limit

### Cash App Taxes (formerly Credit Karma Tax)
- **Federal AND state:** Completely free
- Handles most situations including self-employment
- No income limit
- Limitation: Not available in some states

### TurboTax Free Edition
- Very limited — only W-2 + simple returns
- Many forms require upgrading to paid
- Misleading marketing — read the fine print

### H&R Block Free Online
- Similar to TurboTax — limited free edition
- More complex returns require paid upgrade

## Option 4: VITA (Volunteer Income Tax Assistance)

Free in-person tax prep by IRS-certified volunteers:
- **Income:** Generally under $67,000
- **Available:** February through April 15
- **Locations:** Community centers, libraries, churches
- Find locations: irs.gov/vita

Great for seniors, limited English speakers, or complex situations within income limits.

## Comparison Chart

| Option | Cost | Income Limit | Complex Returns |
|---|---|---|---|
| IRS Free File | Free | $84,000 AGI | Basic |
| IRS Direct File | Free | None | W-2 only |
| FreeTaxUSA | Free (state $15) | None | Yes — all forms |
| Cash App Taxes | Free | None | Most situations |
| VITA | Free | ~$67,000 | In-person help |
| TurboTax Free | Free | Very limited | No |

## What "Free" Actually Covers

Watch for upgrades being pushed:
- "Deluxe" = itemized deductions
- "Premier" = investment income
- "Self-Employed" = business income

TurboTax and H&R Block are notorious for upselling. FreeTaxUSA and Cash App Taxes genuinely cover these for free.

## State Taxes

Federal is free — state varies:
- Some states: Free through IRS Free File partners
- FreeTaxUSA: $14.99 per state
- Cash App Taxes: Free state in supported states
- Many states have their own free filing portals for simple returns

Use our [Federal Income Tax Calculator](/tools/us-federal-income-tax-calculator/) to estimate what you owe before filing.
''',
    },
    {
        'slug': 'estimated-quarterly-taxes-2025-guide',
        'title': 'Quarterly Estimated Taxes 2025: Who Pays, How Much, and When',
        'category': 'us-self-employment',
        'market': 'us',
        'fy_applicable': '2025',
        'reading_time': 8,
        'tags': 'quarterly taxes 2025, estimated tax payments, self employed taxes, 1040-ES',
        'excerpt': 'If you are self-employed, have investment income, or your withholding is not enough, you must pay quarterly estimated taxes. Here are the 2025 due dates, how to calculate payments, and how to avoid the underpayment penalty.',
        'meta_title': 'Quarterly Estimated Taxes 2025: Due Dates, Calculator & Guide',
        'meta_description': 'Quarterly estimated taxes 2025: April 15, June 16, September 15, January 15. How to calculate using safe harbor rules. Form 1040-ES guide for self-employed.',
        'body': '''## Quarterly Estimated Taxes — 2025 Guide

If you receive income without tax withholding — self-employment, freelance, investment, rental, or side income — you generally must pay estimated taxes quarterly.

## 2025 Due Dates

| Quarter | Income Covered | Due Date |
|---|---|---|
| Q1 | Jan 1 – Mar 31 | **April 15, 2025** |
| Q2 | Apr 1 – May 31 | **June 16, 2025** |
| Q3 | Jun 1 – Aug 31 | **September 15, 2025** |
| Q4 | Sep 1 – Dec 31 | **January 15, 2026** |

Note: Q2 covers only 2 months (April–May), not 3. Q4 extends to January.

## Who Must Pay?

You must pay estimated taxes if:
- You expect to owe **at least $1,000** in federal tax after withholding and credits
- AND your withholding covers less than 90% of this year's tax liability OR less than 100% of last year's tax

**Exceptions:**
- If you owed no tax last year and were a US citizen/resident the full year
- Farmers and fishermen (special rules)

## How to Calculate Your Payments

### Method 1: Safe Harbor (Easiest — Avoid Penalty Guaranteed)

Pay 100% of **last year's tax** spread over 4 quarters.

If your AGI was above $150,000 last year: pay **110%** of last year's tax.

**Example:** 2024 tax was $20,000, AGI under $150K:
- Pay $5,000 per quarter ($20,000 ÷ 4)
- Even if you earn more in 2025, no underpayment penalty

### Method 2: 90% of Current Year Tax (More Accurate)

Estimate your 2025 tax and pay 90% across 4 quarters.

**For self-employed:** Include both income tax AND SE tax (15.3%).

**Example:** Expected $100,000 net profit in 2025:
- SE tax: ~$14,130
- Federal income tax (after SE deduction, single): ~$16,000
- Total tax: ~$30,130
- 90% = $27,117
- Per quarter: ~$6,779

### Which Method to Use?

| Situation | Recommendation |
|---|---|
| Income similar to last year | Safe harbor — easy, guaranteed no penalty |
| Income much higher than last year | 90% current year method to avoid big April surprise |
| Income much lower than last year | Safe harbor — pay less now, get refund |

## How to Pay

**Online (IRS Direct Pay):** Free, instant. Pay from checking/savings account.
→ irs.gov/payments

**IRS2Go app:** Mobile payments

**EFTPS (Electronic Federal Tax Payment System):** Schedule future payments, best for recurring quarterly payments.
→ eftps.gov (enrollment takes 1-2 weeks)

**Mail:** Form 1040-ES payment voucher with check

## Underpayment Penalty

If you underpay, the penalty is based on the **underpayment amount × interest rate × period**.

2025 rate: ~8% annualized.

**Example:** Underpaid $5,000 for Q1 (missed April payment, paid in July):
- Penalty: $5,000 × 8% × 3/12 = $100

The penalty is small but adds up across multiple quarters and large amounts.

## State Estimated Taxes

Most states require separate quarterly payments:
- California: April 15, June 15, January 15 (no Q3 Sept payment)
- New York: Same as federal (April, June, September, January)
- Texas, Florida, Nevada: No state income tax — no quarterly payments

## Tracking Your Quarterly Payments

Keep records of:
- Date of each payment
- Amount paid
- Confirmation number (EFTPS or IRS Direct Pay)

When filing your 2025 return, report payments on **Schedule 3, Line 6**. IRS matches these against your 1040.

Use our [Quarterly Estimated Tax Calculator](/tools/us-quarterly-estimated-tax/) to find your exact quarterly amounts.
''',
    },
    {
        'slug': 'home-office-deduction-self-employed-2025',
        'title': 'Home Office Deduction 2025: How to Calculate and Claim It',
        'category': 'us-self-employment',
        'market': 'us',
        'fy_applicable': '2025',
        'reading_time': 7,
        'tags': 'home office deduction, self employed home office, simplified method, Form 8829',
        'excerpt': 'If you are self-employed and work from home, the home office deduction can save hundreds or thousands in taxes. Here is the simplified method, the regular method, and the exclusive-use rule.',
        'meta_title': 'Home Office Deduction 2025: Self-Employed Guide & Calculator',
        'meta_description': 'Home office deduction 2025 for self-employed. Simplified method ($5/sqft, max $1,500) vs regular method (actual expenses). Exclusive use rule. Form 8829.',
        'body': '''## Home Office Deduction 2025 — Self-Employed Only

The home office deduction allows self-employed individuals to deduct a portion of home expenses when they use part of their home regularly and exclusively for business.

**W-2 employees:** This deduction is NOT available since 2018 (Tax Cuts and Jobs Act).

## The Exclusive-Use Requirement

The space must be used:
1. **Regularly** — not just occasionally
2. **Exclusively** — only for business, not personal use

A dedicated room used only as an office qualifies. A dining table you sometimes work at does NOT qualify.

**Exception:** Inventory storage and daycare facilities have relaxed rules.

## Method 1: Simplified Method (Most Popular)

**Deduction:** $5 per square foot of home office space, up to **300 sq ft**
**Maximum deduction:** $1,500 per year

**Example:**
- Home office: 200 sq ft
- Deduction: 200 × $5 = **$1,000**

**Pros:** Simple, no need to track actual expenses
**Cons:** Usually gives a smaller deduction

## Method 2: Regular Method (Larger Deduction)

Calculate your business-use percentage:
- **Business %** = (Office sq ft) ÷ (Total home sq ft)

Apply this percentage to actual home expenses:

| Expense | Annual Amount | Business % | Deduction |
|---|---|---|---|
| Mortgage interest | $18,000 | 15% | $2,700 |
| Utilities | $3,600 | 15% | $540 |
| Insurance | $1,800 | 15% | $270 |
| Repairs | $500 | 15% | $75 |
| Depreciation | $4,000 | 15% | $600 |
| **Total** | | | **$4,185** |

**Example:** 300 sq ft office in a 2,000 sq ft home = 15% business use

File using **Form 8829**. The remaining mortgage interest and property taxes are deducted on Schedule A (if itemizing).

## Depreciation — A Big Deduction Worth Calculating

Your home depreciates over 39 years (non-residential rate for home office). The depreciation deduction can be significant:

- Home purchase price: $400,000
- Land value (not depreciable): $80,000
- Building value: $320,000
- Annual depreciation: $320,000 ÷ 39 = $8,205
- Business % 15%: $8,205 × 15% = **$1,231 deduction**

**Warning:** Depreciation taken must be "recaptured" (taxed at 25%) when you sell the home. Track it carefully.

## Which Method Is Better?

**Simplified wins if:**
- Your home expenses are low (renters in low-cost areas)
- Your office is small
- You want simplicity

**Regular wins if:**
- You have a large office and high home expenses
- You own your home with mortgage interest + depreciation
- Your office is >300 sq ft

**Run both calculations to decide.** You can switch methods each year.

## Deduction Limit — Cannot Create a Loss

Home office deduction cannot exceed your net business income. Unused deduction (regular method) carries forward to the next year.

Under the simplified method, unused deduction does NOT carry forward.

## Renting Your Home

If you rent, use the regular method:
- Apply business % to annual rent
- Apply business % to renter's insurance
- Apply business % to utilities

**Example:** $1,500/month rent, 15% office use = $2,700 deduction

## Record Keeping

Keep records of:
- Floor plan or measurement of office space and total home
- Utility bills, insurance, repairs
- Photos of the dedicated office space
- Mortgage statements or lease agreement

The IRS has historically scrutinized home office deductions — clear, consistent records are essential.
''',
    },
]


class Command(BaseCommand):
    help = 'Seed 10 additional US blog articles'

    def handle(self, *args, **options):
        self.stdout.write('Seeding extra US blog articles...')

        author = Author.objects.filter(name='Sarah Mitchell').first()
        if not author:
            author = Author.objects.create(
                name='Sarah Mitchell',
                title='Enrolled Agent (EA) & Tax Advisor',
                bio=('Sarah Mitchell is an IRS-licensed Enrolled Agent with 12 years of experience in '
                     'federal and state tax planning. She specializes in self-employment tax, freelancer '
                     'finances, and investment taxation.'),
                is_ca=False,
            )
            self.stdout.write(f'  Created author: {author.name}')

        US_CAT_NAMES = {
            'us-income-tax':      'US Income Tax',
            'us-self-employment': 'US Self-Employment',
            'us-investments':     'US Investments',
            'us-tax-guides':      'US Tax Guides',
        }

        # Fix / create categories with correct names
        cat_map = {}
        for slug, name in US_CAT_NAMES.items():
            cat, _ = Category.objects.update_or_create(
                slug=slug,
                defaults={'name': name, 'description': ''},
            )
            cat_map[slug] = cat
            self.stdout.write(f'  Category: {cat.name}')

        for i, art in enumerate(ARTICLES, 1):
            cat_slug = art.pop('category')
            cat = cat_map.get(cat_slug)

            obj, created = Article.objects.get_or_create(
                slug=art['slug'],
                defaults={
                    'title': art['title'],
                    'author': author,
                    'category': cat,
                    'market': art.get('market', 'us'),
                    'fy_applicable': art.get('fy_applicable', '2025'),
                    'tags': art.get('tags', ''),
                    'body': art['body'],
                    'excerpt': art['excerpt'],
                    'meta_title': art['meta_title'],
                    'meta_description': art['meta_description'],
                    'reading_time': art.get('reading_time', 7),
                    'is_featured': art.get('is_featured', False),
                    'is_published': True,
                    'published_at': timezone.now(),
                },
            )
            self.stdout.write(f'  [{i:02d}] {obj.title[:60]} ({"created" if created else "exists"})')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. US articles total: {Article.objects.filter(market="us").count()}'
        ))
