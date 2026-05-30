"""
Seed US tax blog articles — Tax Year 2025
10 high-traffic, SEO-optimized articles targeting top US tax search terms.
Run: python manage.py seed_us_blog
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import Article, Author, Category


US_CATEGORIES = [
    {'name': 'US Income Tax',      'slug': 'us-income-tax',      'description': 'Federal income tax guides for US taxpayers'},
    {'name': 'US Self-Employment', 'slug': 'us-self-employment',  'description': 'Tax guides for freelancers and 1099 contractors'},
    {'name': 'US Investments',     'slug': 'us-investments',      'description': 'Capital gains, dividends, and investment tax strategies'},
    {'name': 'US Tax Guides',      'slug': 'us-tax-guides',       'description': 'Complete how-to guides for US taxpayers'},
]

US_AUTHOR = {
    'name': 'Sarah Mitchell',
    'title': 'Enrolled Agent (EA) & Tax Advisor',
    'bio': ('Sarah Mitchell is an IRS-licensed Enrolled Agent with 12 years of experience in '
            'federal and state tax planning. She specializes in self-employment tax, freelancer '
            'finances, and investment taxation. Sarah has helped thousands of Americans navigate '
            'the US tax system and reduce their tax bills legally.'),
    'is_ca': False,
}

ARTICLES = [
    {
        'slug': 'self-employment-tax-2025-guide',
        'title': 'Self-Employment Tax 2025: How to Calculate SE Tax (15.3% Explained)',
        'category': 'us-self-employment',
        'market': 'us',
        'fy_applicable': '2025',
        'is_featured': True,
        'reading_time': 8,
        'tags': 'self employment tax, SE tax 2025, 1099 tax, freelancer taxes',
        'excerpt': ('Self-employment tax in 2025 is 15.3% — but you only pay it on 92.35% of '
                    'your net profit, and you get to deduct half of it from your income tax. '
                    'Here is exactly how it works, with a step-by-step calculation example.'),
        'meta_title': 'Self-Employment Tax 2025: How to Calculate SE Tax (15.3%)',
        'meta_description': ('Self-employment tax 2025 is 15.3% on 92.35% of net profit. '
                             'Learn how SE tax works, how to calculate it, and how to deduct '
                             'half of it from your income taxes. With examples.'),
        'body': '''## What Is Self-Employment Tax?

Self-employment tax (SE tax) is the self-employed person's version of FICA — the Social Security and Medicare taxes that W-2 employees split with their employer. When you are self-employed, you pay both the employee and employer share yourself.

**SE Tax Rate 2025: 15.3%**

| Component | Rate | Wage Cap |
|-----------|------|----------|
| Social Security | 12.4% | $176,100 |
| Medicare | 2.9% | No cap |
| **Total SE Tax** | **15.3%** | — |

Above $200,000 in net earnings (single filers), you also owe an additional **0.9% Medicare tax**.

---

## Who Must Pay SE Tax?

You owe SE tax if your **net self-employment income is $400 or more** in 2025. This includes:

- Freelancers and independent contractors (1099-NEC income)
- Sole proprietors (Schedule C filers)
- Partners in a partnership
- Members of an LLC taxed as a partnership
- Gig workers (Uber, DoorDash, Etsy, Fiverr, etc.)

---

## How to Calculate SE Tax — Step by Step

**Example:** You earned $80,000 net profit from freelancing in 2025.

### Step 1: Calculate SE Net Earnings
$$80,000 \times 0.9235 = \$73,880$$

The IRS only taxes 92.35% of your net profit to account for the employer-equivalent deduction.

### Step 2: Calculate Social Security Tax
$$\$73,880 \times 12.4\% = \$9,161$$

(Capped at $176,100 × 12.4% = $21,836 maximum)

### Step 3: Calculate Medicare Tax
$$\$73,880 \times 2.9\% = \$2,143$$

### Step 4: Total SE Tax
$$\$9,161 + \$2,143 = \$11,304$$

### Step 5: Deductible Amount
You can deduct **50% of SE tax** from your gross income:
$$\$11,304 \times 50\% = \$5,652$$

This reduces your **adjusted gross income (AGI)** before calculating federal income tax.

---

## Real Tax Example: $80,000 Freelance Income

| Item | Amount |
|------|--------|
| Net self-employment profit | $80,000 |
| SE net earnings (× 92.35%) | $73,880 |
| SE tax (15.3%) | $11,304 |
| SE tax deduction (50%) | -$5,652 |
| Adjusted income for federal tax | $74,348 |
| Standard deduction (single) | -$15,000 |
| Taxable income | $59,348 |
| Federal income tax | ~$8,636 |
| **Total tax (SE + federal)** | **~$19,940** |
| Effective total rate | **~24.9%** |
| Quarterly payment (÷ 4) | ~$4,985 |

---

## The SE Tax Deduction: Your Most Important Write-Off

You deduct **50% of your SE tax** on Schedule 1, Line 15 of Form 1040. This is an **above-the-line deduction** — it reduces your AGI whether you itemize or take the standard deduction.

In our example: deducting $5,652 saves you approximately $5,652 × 22% = **$1,243 in federal income tax**.

---

## Quarterly Estimated Tax Payments

As a self-employed person, you must pay taxes quarterly (not at year end). The 2025 due dates are:

| Quarter | Income Period | Due Date |
|---------|--------------|----------|
| Q1 | Jan 1 – Mar 31 | April 15, 2025 |
| Q2 | Apr 1 – May 31 | June 16, 2025 |
| Q3 | Jun 1 – Aug 31 | September 15, 2025 |
| Q4 | Sep 1 – Dec 31 | January 15, 2026 |

**Safe harbor rule:** Pay at least 100% of last year's tax (110% if your prior year income exceeded $150,000) to avoid underpayment penalties.

---

## 5 Ways to Reduce Your SE Tax Legally

1. **Maximize business deductions** — Every dollar of business expense reduces your net profit and SE tax base. Home office, equipment, software, health insurance, retirement contributions.

2. **Contribute to a SEP-IRA or Solo 401(k)** — Up to 25% of net profit (SEP-IRA) or $23,500 employee + 25% employer match (Solo 401k) in 2025. These reduce taxable income but **not** SE tax.

3. **Elect S-Corp status** — Once income exceeds ~$50,000–$60,000, an S-Corp election lets you split income between salary (subject to FICA) and distributions (not subject to SE tax). Consult a CPA first.

4. **Self-employed health insurance deduction** — 100% of health insurance premiums are deductible from income (not from SE tax), saving significant taxes.

5. **Home office deduction** — If you use part of your home exclusively for business, deduct the proportional costs.

---

## Use Our SE Tax Calculator

Use our [Self-Employment Tax Calculator](/tools/us-self-employment-tax-calculator/) to instantly calculate:
- Your exact SE tax for 2025
- Federal income tax after the SE deduction
- Total tax liability
- Quarterly payment amounts

**Disclaimer:** This guide is for informational purposes. Tax laws change. Consult an Enrolled Agent or CPA for advice specific to your situation.
''',
    },
    {
        'slug': 'federal-income-tax-brackets-2025',
        'title': 'Federal Income Tax Brackets 2025: Complete Guide (All Filing Statuses)',
        'category': 'us-income-tax',
        'market': 'us',
        'fy_applicable': '2025',
        'is_featured': True,
        'reading_time': 7,
        'tags': 'federal tax brackets 2025, income tax rates 2025, tax brackets single married',
        'excerpt': ('The 2025 federal income tax brackets range from 10% to 37%. Your filing '
                    'status determines which bracket thresholds apply to you. Here are the '
                    'exact numbers for Single, Married Filing Jointly, HOH, and MFS filers.'),
        'meta_title': 'Federal Income Tax Brackets 2025: Single, MFJ, HOH, MFS Rates',
        'meta_description': ('2025 federal income tax brackets for all filing statuses. '
                             'See exact thresholds for Single ($11,925–$626,350), MFJ, HOH, '
                             'and MFS. How progressive tax works with examples.'),
        'body': '''## 2025 Federal Tax Brackets — Overview

The US uses a **progressive tax system** — you only pay the higher rate on income *above* each threshold, not on your entire income.

**Tax rates in 2025:** 10%, 12%, 22%, 24%, 32%, 35%, 37%

---

## Single Filers — 2025 Tax Brackets

| Tax Rate | Income Range | Tax Owed |
|----------|-------------|----------|
| 10% | $0 – $11,925 | 10% of taxable income |
| 12% | $11,926 – $48,475 | $1,192.50 + 12% of amount over $11,925 |
| 22% | $48,476 – $103,350 | $5,578.50 + 22% of amount over $48,475 |
| 24% | $103,351 – $197,300 | $17,651.50 + 24% of amount over $103,350 |
| 32% | $197,301 – $250,525 | $40,199.50 + 32% of amount over $197,300 |
| 35% | $250,526 – $626,350 | $57,231.50 + 35% of amount over $250,525 |
| 37% | Over $626,350 | $188,769.75 + 37% of amount over $626,350 |

**Standard deduction (single): $15,000**

---

## Married Filing Jointly — 2025 Tax Brackets

| Tax Rate | Income Range |
|----------|-------------|
| 10% | $0 – $23,850 |
| 12% | $23,851 – $96,950 |
| 22% | $96,951 – $206,700 |
| 24% | $206,701 – $394,600 |
| 32% | $394,601 – $501,050 |
| 35% | $501,051 – $751,600 |
| 37% | Over $751,600 |

**Standard deduction (MFJ): $30,000**

---

## Head of Household — 2025 Tax Brackets

| Tax Rate | Income Range |
|----------|-------------|
| 10% | $0 – $17,000 |
| 12% | $17,001 – $64,850 |
| 22% | $64,851 – $103,350 |
| 24% | $103,351 – $197,300 |
| 32% | $197,301 – $250,500 |
| 35% | $250,501 – $626,350 |
| 37% | Over $626,350 |

**Standard deduction (HOH): $22,500**

---

## Married Filing Separately — 2025 Tax Brackets

| Tax Rate | Income Range |
|----------|-------------|
| 10% | $0 – $11,925 |
| 12% | $11,926 – $48,475 |
| 22% | $48,476 – $103,350 |
| 24% | $103,351 – $197,300 |
| 32% | $197,301 – $250,525 |
| 35% | $250,526 – $375,800 |
| 37% | Over $375,800 |

**Standard deduction (MFS): $15,000**

---

## How Progressive Tax Works — Example

**Single filer, $75,000 gross income, standard deduction:**

Taxable income: $75,000 – $15,000 = **$60,000**

| Bracket | Income in Bracket | Tax |
|---------|------------------|-----|
| 10% | $11,925 | $1,192.50 |
| 12% | $36,550 ($48,475 – $11,925) | $4,386 |
| 22% | $11,525 ($60,000 – $48,475) | $2,535.50 |
| **Total** | | **$8,114** |

- **Effective tax rate:** $8,114 ÷ $75,000 = **10.8%**
- **Marginal tax rate:** 22% (the rate on your last dollar)
- **Take-home:** $75,000 – $8,114 = **$66,886** (before FICA)

---

## Key Takeaways

- Your **marginal rate** is only the rate on income above a threshold — not your entire income
- Most middle-income Americans pay an **effective rate of 12–22%**, not 37%
- The standard deduction significantly reduces how much income is taxed
- Filing jointly as a married couple almost always results in lower taxes than filing separately

Use our [Federal Income Tax Calculator](/tools/us-federal-income-tax-calculator/) to calculate your exact 2025 tax bill in seconds.

**Disclaimer:** Based on IRS Rev. Proc. 2024-40. Consult a tax professional for personalized advice.
''',
    },
    {
        'slug': 'standard-deduction-2025-should-you-itemize',
        'title': 'Standard Deduction 2025: $15,000 Single, $30,000 MFJ — Should You Itemize?',
        'category': 'us-income-tax',
        'market': 'us',
        'fy_applicable': '2025',
        'is_featured': True,
        'reading_time': 6,
        'tags': 'standard deduction 2025, itemized deductions, should I itemize, SALT cap',
        'excerpt': ('The 2025 standard deduction is $15,000 for single filers and $30,000 for '
                    'married filing jointly. Most Americans take it — but if you have a big '
                    'mortgage, live in a high-tax state, or donate heavily, itemizing might save '
                    'you more. Here is how to decide.'),
        'meta_title': 'Standard Deduction 2025: $15,000 Single, $30,000 MFJ vs Itemizing',
        'meta_description': ('2025 standard deduction is $15,000 (single) and $30,000 (MFJ). '
                             'Should you itemize instead? See the SALT cap, mortgage interest, '
                             'and charitable deduction rules. With decision tool.'),
        'body': '''## 2025 Standard Deduction Amounts

| Filing Status | Standard Deduction |
|--------------|-------------------|
| Single | **$15,000** |
| Married Filing Jointly | **$30,000** |
| Married Filing Separately | **$15,000** |
| Head of Household | **$22,500** |

These are up from $14,600 (single) and $29,200 (MFJ) in 2024 — a 2.7% inflation adjustment.

---

## Who Should Take the Standard Deduction?

**Take standard if:** Your total itemizable deductions are less than the standard deduction for your filing status.

The majority of Americans take the standard deduction — the Tax Cuts and Jobs Act (TCJA) roughly doubled it in 2018, making itemizing worthwhile for far fewer people.

---

## What Can You Itemize? (Schedule A Deductions)

### 1. State and Local Taxes (SALT) — Capped at $10,000

You can deduct state income taxes + property taxes, but only up to **$10,000 total** (TCJA cap, currently through 2025). This cap hits residents of high-tax states like California, New York, and New Jersey hardest.

### 2. Mortgage Interest

Deductible on loans up to **$750,000** (loans taken after Dec 15, 2017). If your mortgage was before that date, the $1,000,000 limit may apply. From Form 1098.

### 3. Charitable Contributions

Cash donations to qualified organizations (churches, nonprofits, schools) are fully deductible up to 60% of AGI. Noncash donations follow different rules.

### 4. Medical and Dental Expenses

Only the amount exceeding **7.5% of your AGI** is deductible. Example: $80,000 AGI → first $6,000 of medical expenses are not deductible.

### 5. Casualty and Theft Losses

Limited to federally declared disasters only.

---

## When Itemizing Beats the Standard Deduction

**Example: Homeowner in California, single filer, $120,000 income**

| Deduction | Amount |
|-----------|--------|
| Mortgage interest (Form 1098) | $14,000 |
| SALT (state income + property tax) | $10,000 (capped) |
| Charitable donations | $3,500 |
| **Total itemized** | **$27,500** |
| Standard deduction | $15,000 |
| **Better choice** | **Itemize ($27,500)** |
| **Extra deduction vs standard** | $12,500 |
| **Tax savings at 22% bracket** | ~$2,750 |

---

## The SALT Cap Problem for High-Tax States

If you live in California, New York, New Jersey, or Massachusetts, you likely pay more than $10,000 in state income + property taxes alone. The $10,000 SALT cap (expiring after 2025) limits what you can deduct. This significantly reduces the value of itemizing for many residents of these states.

**Note:** The TCJA's individual provisions — including the SALT cap and higher standard deduction — are currently set to expire after 2025. Congress may extend them. Watch for legislative updates.

---

## How to Decide: A Simple Rule

**Itemize if:** Mortgage interest + SALT (up to $10K) + charitable + medical (above 7.5% AGI) > Your standard deduction.

Otherwise, take the standard deduction — it is simpler and likely saves you more.

Use our [Standard vs Itemized Deduction Calculator](/tools/us-standard-vs-itemized-deduction/) to compare your exact numbers instantly.
''',
    },
    {
        'slug': 'quarterly-estimated-taxes-2025-guide',
        'title': 'Quarterly Estimated Taxes 2025: Due Dates, How to Calculate, Safe Harbor',
        'category': 'us-self-employment',
        'market': 'us',
        'fy_applicable': '2025',
        'is_featured': True,
        'reading_time': 7,
        'tags': 'quarterly estimated tax 2025, estimated tax due dates, safe harbor rule, Form 1040-ES',
        'excerpt': ('If you are self-employed, have investment income, or receive income without '
                    'withholding, you likely need to pay quarterly estimated taxes. The 2025 '
                    'due dates are April 15, June 16, September 15, and January 15, 2026. '
                    'Here is how to calculate and pay.'),
        'meta_title': 'Quarterly Estimated Taxes 2025: Due Dates & How to Calculate',
        'meta_description': ('2025 quarterly estimated tax due dates: April 15, June 16, Sep 15, '
                             'Jan 15 2026. How to calculate payments, safe harbor rule, and how '
                             'to pay the IRS. For freelancers, investors, and self-employed.'),
        'body': '''## Who Needs to Pay Quarterly Estimated Taxes?

You must pay quarterly estimated taxes if you expect to owe **$1,000 or more** in federal tax for 2025 after withholding and refundable credits. This typically applies to:

- Freelancers and independent contractors (1099 income)
- Self-employed business owners
- Investors with significant dividends, capital gains, or rental income
- Employees with large side income not covered by withholding
- Retirees with pension, Social Security, or investment income

---

## 2025 Quarterly Tax Due Dates

| Quarter | Income Period | Due Date |
|---------|--------------|----------|
| Q1 | January 1 – March 31 | **April 15, 2025** |
| Q2 | April 1 – May 31 | **June 16, 2025** |
| Q3 | June 1 – August 31 | **September 15, 2025** |
| Q4 | September 1 – December 31 | **January 15, 2026** |

Note: Q2 is due June 16 (not June 15) because June 15 falls on a Sunday in 2025.

---

## How to Calculate Your Quarterly Payments

### Method 1: Estimate Current Year Tax (Simplest)

1. Estimate your 2025 annual income (net of business deductions)
2. Calculate expected federal + SE tax
3. Divide by 4 → pay each quarter

**Example: $90,000 freelance income, single**
- SE tax: $90,000 × 92.35% × 15.3% = ~$12,716
- SE deduction (50%): $6,358
- Taxable income: $90,000 – $6,358 – $15,000 std ded = $68,642
- Federal income tax: ~$10,474
- Total annual tax: $12,716 + $10,474 = **$23,190**
- Quarterly payment: $23,190 ÷ 4 = **$5,797**

### Method 2: Safe Harbor (Avoids Underpayment Penalty)

The **safe harbor rule** protects you from underpayment penalties if you pay:

- **100%** of your prior year's total tax, OR
- **110%** of prior year tax (if your prior year AGI exceeded $150,000)

**Example:** If your 2024 total tax (Form 1040, Line 24) was $18,000, pay $18,000 ÷ 4 = **$4,500/quarter** regardless of what you earn in 2025. No penalty even if you end up owing more.

---

## How to Pay Estimated Taxes

**Option 1: IRS Direct Pay (Free)**
Pay online at [irs.gov/payments](https://www.irs.gov/payments). No account needed, instant confirmation.

**Option 2: EFTPS (Electronic Federal Tax Payment System)**
Free IRS service. Requires enrollment. Best for recurring payments.

**Option 3: Pay by check (Form 1040-ES)**
Download Form 1040-ES, write your SSN and "2025 Form 1040-ES" on the check, mail to IRS.

**Option 4: IRS2Go mobile app**
Same as Direct Pay but on your phone.

---

## Common Mistakes

**Mistake 1: Paying quarterly income but forgetting SE tax**
SE tax (15.3%) is a significant portion of your tax bill. Include it in your quarterly calculation.

**Mistake 2: Using gross income instead of net profit**
Only your profit (after business expenses) is subject to SE tax and income tax.

**Mistake 3: Missing the safe harbor**
If you had a profitable prior year, safe harbor payments protect you from penalties even in a slow year.

**Mistake 4: Skipping Q2 (it's due in June, not July)**
Q2 covers only April–May income, but is due June 16 — earlier than many people expect.

---

Use our [Quarterly Estimated Tax Calculator](/tools/us-quarterly-estimated-tax/) to get your exact payment amounts and a safe harbor calculation.
''',
    },
    {
        'slug': 'capital-gains-tax-2025-guide',
        'title': 'Capital Gains Tax 2025: Short-Term vs Long-Term Rates + How to Minimize',
        'category': 'us-investments',
        'market': 'us',
        'fy_applicable': '2025',
        'is_featured': True,
        'reading_time': 9,
        'tags': 'capital gains tax 2025, long term capital gains, short term capital gains, NIIT',
        'excerpt': ('Capital gains tax in 2025 depends on how long you held the asset. '
                    'Short-term gains (under 1 year) are taxed as ordinary income (up to 37%). '
                    'Long-term gains get preferential rates: 0%, 15%, or 20%. Plus a potential '
                    '3.8% NIIT. Here is the complete guide.'),
        'meta_title': 'Capital Gains Tax 2025: Short-Term vs Long-Term Rates Explained',
        'meta_description': ('Capital gains tax 2025: short-term taxed as ordinary income (37% max), '
                             'long-term preferential rates 0%/15%/20% plus 3.8% NIIT. '
                             'With calculation examples for stocks, crypto, and real estate.'),
        'body': '''## Two Types of Capital Gains

When you sell an asset (stocks, crypto, real estate, ETFs) for a profit, you owe capital gains tax. The rate depends on **how long you held it**.

| Holding Period | Type | Tax Rate |
|---------------|------|----------|
| 1 year or less | Short-term | Ordinary income rates (10%–37%) |
| More than 1 year | Long-term | Preferential rates (0%, 15%, or 20%) |

Holding for just one extra day can dramatically reduce your tax bill. This is the most powerful tax-timing strategy available to investors.

---

## 2025 Long-Term Capital Gains Rates

### Single Filers
| Rate | Taxable Income |
|------|---------------|
| 0% | $0 – $48,350 |
| 15% | $48,351 – $533,400 |
| 20% | Over $533,400 |

### Married Filing Jointly
| Rate | Taxable Income |
|------|---------------|
| 0% | $0 – $96,700 |
| 15% | $96,701 – $600,050 |
| 20% | Over $600,050 |

### Head of Household
| Rate | Taxable Income |
|------|---------------|
| 0% | $0 – $64,750 |
| 15% | $64,751 – $566,700 |
| 20% | Over $566,700 |

---

## The 3.8% Net Investment Income Tax (NIIT)

If your **modified AGI exceeds** $200,000 (single) or $250,000 (MFJ), you owe an additional **3.8% NIIT** on the lesser of:
- Your net investment income, OR
- The amount your MAGI exceeds the threshold

**This effectively makes the maximum long-term capital gains rate 23.8% for high earners** (20% + 3.8% NIIT).

---

## Real Examples

### Example 1: Long-term stock gain, moderate income

- Annual W-2 income: $60,000 (single)
- Long-term stock gain: $20,000
- Total income: $80,000
- LTCG rate: **15%** (you're between $48,350 and $533,400)
- LTCG tax: $20,000 × 15% = **$3,000**

### Example 2: The 0% Rate — A Powerful Strategy

- Retired couple, MFJ, other income: $40,000
- Long-term gains: $50,000
- Total income: $90,000 (under $96,700 threshold)
- LTCG rate: **0%**
- LTCG tax: **$0**

This is why "tax gain harvesting" — deliberately selling appreciated assets in low-income years — is such a powerful strategy for retirees and early retirees.

### Example 3: Short-term gain danger

- Annual income: $100,000 (single, 22% marginal bracket)
- Short-term stock gain: $20,000
- Additional tax: $20,000 × 22% = **$4,400**
- If held one more year (long-term): $20,000 × 15% = **$3,000**
- Saving from holding longer: **$1,400**

---

## Capital Gains on Crypto

Cryptocurrency is treated as **property** by the IRS — the same rules apply:
- Short-term (under 1 year): ordinary income rates
- Long-term (over 1 year): 0%/15%/20% LTCG rates

You must report every taxable crypto event: selling, trading crypto-for-crypto, using crypto to buy goods/services. Transfers between your own wallets are not taxable.

---

## Capital Gains on Real Estate

### Primary Residence Exclusion
If you lived in your home for **at least 2 of the last 5 years**, you can exclude:
- **$250,000** of gain (single)
- **$500,000** of gain (MFJ)

This is one of the largest tax breaks available to homeowners.

### Rental Property
Gains on rental property are taxable capital gains. Additionally, **depreciation recapture** (the depreciation deductions you claimed) is taxed at a maximum of 25%.

---

## Strategies to Reduce Capital Gains Tax

1. **Hold for over 1 year** — Most impactful. Converts 37% max to 20% max.

2. **Tax-loss harvesting** — Sell losing positions to offset gains. Losses offset gains dollar-for-dollar, then up to $3,000 of ordinary income per year. Remaining losses carry forward.

3. **Time gains to a low-income year** — Retiring, taking time off, starting a business? Realize gains when your income is low to hit the 0% LTCG bracket.

4. **Max out tax-advantaged accounts** — Gains inside 401(k), IRA, HSA grow tax-free or tax-deferred.

5. **Donate appreciated stock** — Donating stock directly to charity avoids capital gains AND gives you a charitable deduction for the full market value.

Use our [Capital Gains Tax Calculator](/tools/us-capital-gains-tax-calculator/) to see your exact tax for 2025.
''',
    },
    {
        'slug': '1099-vs-w2-tax-differences-2025',
        'title': '1099 vs W-2: Tax Differences and What You Actually Owe as a Freelancer',
        'category': 'us-self-employment',
        'market': 'us',
        'fy_applicable': '2025',
        'is_featured': False,
        'reading_time': 7,
        'tags': '1099 vs w2, freelancer taxes, independent contractor taxes, 1099 income',
        'excerpt': ('The difference between 1099 and W-2 income is bigger than most people '
                    'realize. As a 1099 contractor you pay self-employment tax on top of income '
                    'tax — but you also get powerful deductions that W-2 employees do not. '
                    'Here is the full comparison.'),
        'meta_title': '1099 vs W-2: Tax Differences — What Freelancers Actually Owe',
        'meta_description': ('1099 vs W-2 taxes: freelancers pay 15.3% SE tax but get business '
                             'deductions W-2 employees cannot. Full comparison of tax burden, '
                             'deductions, and quarterly payment requirements for 2025.'),
        'body': '''## The Core Difference

| | W-2 Employee | 1099 Contractor |
|--|-------------|----------------|
| Who files taxes | Employer withholds, files W-2 | You file Schedule C |
| Social Security | 6.2% (employer pays other 6.2%) | 12.4% (you pay both shares) |
| Medicare | 1.45% | 2.9% |
| Quarterly payments | Not usually required | Required |
| Business deductions | Very limited | Extensive |
| Benefits (health, 401k) | Often employer-provided | Self-funded |

---

## The SE Tax Burden for 1099 Workers

A W-2 employee earning $80,000 pays:
- FICA (employee share): 6.2% SS + 1.45% Medicare = **$6,000**
- Their employer pays another $6,000 in FICA (invisible to the employee)

A 1099 contractor earning $80,000 pays:
- Self-employment tax: 15.3% on 92.35% of $80,000 = **$11,304**
- But deducts half ($5,652) from income taxes

**Net extra burden:** ~$5,304 more in SE tax vs a W-2 worker — but partially offset by business deductions.

---

## Deductions that 1099 Workers Get (W-2 Employees Do Not)

This is where 1099 income gets its advantages:

| Deduction | Limit | Notes |
|-----------|-------|-------|
| Home office | Proportional | Must be used exclusively and regularly for business |
| Business equipment | 100% (Section 179) | Computers, cameras, tools, etc. |
| Software & subscriptions | 100% | Adobe, Slack, Notion, etc. |
| Health insurance premiums | 100% | Self-employed health insurance deduction |
| Self-employed retirement | Up to $70,000 | SEP-IRA or Solo 401(k) |
| Business travel | 100% | Flights, hotels, car rental for business |
| Vehicle (business use) | Actual or standard mileage | 70 cents/mile standard rate |
| Professional development | 100% | Courses, books, conferences |
| Half of SE tax | 50% of SE tax | Above-the-line deduction |

---

## Break-Even Analysis: When Does 1099 Pay More?

**W-2 at $80,000 vs 1099 at $80,000 (single filer, standard deduction):**

| | W-2 | 1099 |
|--|-----|------|
| Gross income | $80,000 | $80,000 |
| SE tax | $0 | $11,304 |
| SE deduction | — | -$5,652 |
| Standard deduction | -$15,000 | -$15,000 |
| Taxable income | $65,000 | $59,348 |
| Federal income tax | ~$9,998 | ~$8,636 |
| FICA (employee) | ~$6,000 | included above |
| **Total tax** | **~$15,998** | **~$19,940** |
| **Extra 1099 burden** | | **~$3,942** |

That $3,942 gap can easily be closed with legitimate business deductions — home office, equipment, software, health insurance, and retirement contributions.

---

## Quarterly Payments: The Biggest Practical Difference

W-2 workers have taxes withheld automatically. As a 1099 worker, you must pay quarterly:

| Due Date | Coverage |
|----------|----------|
| April 15, 2025 | Q1 income |
| June 16, 2025 | Q2 income |
| September 15, 2025 | Q3 income |
| January 15, 2026 | Q4 income |

**Pro tip:** Set aside 25–30% of every payment you receive in a separate savings account. Pay estimated taxes from this account each quarter.

---

## Which Is Better: 1099 or W-2?

Neither is inherently better — it depends on your situation:

**1099 wins if:**
- You have significant business expenses to deduct
- You can fund your own health insurance and retirement
- You value flexibility and rate control
- Your 1099 rate is at least 20–30% higher than equivalent W-2 salary

**W-2 wins if:**
- Your employer offers strong benefits (health insurance, 401k match)
- You prefer predictable paycheck withholding
- You have few deductible expenses

Use our [Self-Employment Tax Calculator](/tools/us-self-employment-tax-calculator/) to see your exact 1099 tax burden.
''',
    },
    {
        'slug': 'how-to-reduce-taxes-2025',
        'title': '10 Legal Ways to Reduce Your Tax Bill in 2025',
        'category': 'us-tax-guides',
        'market': 'us',
        'fy_applicable': '2025',
        'is_featured': False,
        'reading_time': 8,
        'tags': 'reduce taxes 2025, tax saving strategies, tax deductions 2025, lower tax bill',
        'excerpt': ('The US tax code is filled with legal ways to reduce what you owe — '
                    'retirement accounts, HSAs, tax-loss harvesting, deductions, and timing '
                    'strategies. Here are 10 moves that actually work in 2025, ranked by '
                    'impact.'),
        'meta_title': '10 Legal Ways to Reduce Your Tax Bill in 2025',
        'meta_description': ('10 proven strategies to legally reduce your 2025 federal taxes: '
                             '401k/IRA contributions, HSA, tax-loss harvesting, home office, '
                             'charitable giving, timing capital gains, and more.'),
        'body': '''## 1. Max Out Your 401(k) — $23,500 Pre-Tax

The single most impactful move for most employees. Every dollar into your traditional 401(k) reduces your taxable income dollar-for-dollar.

- **2025 limit:** $23,500 ($31,000 if age 50+)
- **Tax savings at 22% bracket:** $23,500 × 22% = **$5,170 saved**
- **At 24% bracket:** $5,640 saved

If your employer matches, the effective return before any investment growth is effectively 100% on matched contributions.

---

## 2. Contribute to a Traditional IRA — $7,000

If you qualify (income limits apply for deductibility), a traditional IRA contribution reduces taxable income by up to $7,000 ($8,000 if 50+).

**2025 IRA deductibility phaseout:**
- Single covered by workplace plan: $79,000–$89,000 MAGI
- MFJ, covered by workplace plan: $126,000–$146,000 MAGI

Consider a **Roth IRA** if you expect to be in a higher bracket in retirement — no current deduction, but all growth is tax-free.

---

## 3. Max Out Your HSA — $4,300 Single / $8,550 Family

The Health Savings Account is the only triple-tax-advantaged account:
- **Contributions are pre-tax** (reduce taxable income)
- **Growth is tax-free**
- **Withdrawals for medical expenses are tax-free**

You must have a High-Deductible Health Plan (HDHP). Unused HSA balances roll over forever — it becomes a de facto retirement account at 65.

---

## 4. Self-Employed? Open a SEP-IRA or Solo 401(k)

If you are self-employed, you can contribute up to **$70,000 in 2025** to a Solo 401(k) (employee + employer contributions). A SEP-IRA allows up to 25% of net self-employment income.

For someone earning $100,000 net profit, a $25,000 SEP-IRA contribution saves approximately $5,500+ in federal + SE-adjacent taxes.

---

## 5. Tax-Loss Harvesting

Sell investments that are down in value to realize a loss that offsets your capital gains. Rules:
- Losses offset capital gains dollar-for-dollar
- Net losses up to $3,000 can offset ordinary income per year
- Excess losses carry forward to future years
- Watch the **30-day wash sale rule** — do not buy substantially identical securities within 30 days before or after selling at a loss

---

## 6. Bunch Charitable Deductions

The standard deduction is high enough that many people can not itemize every year. Solution: **bunch** two or three years of donations into one year to exceed the standard deduction threshold, then take standard in alternate years.

**Better:** Donate appreciated stock directly to charity. You avoid capital gains AND get a deduction for the full market value.

---

## 7. Home Office Deduction (Remote Workers / Self-Employed)

If you use part of your home **exclusively and regularly** for business, deduct the proportional costs:
- **Simplified method:** $5 per square foot, up to 300 sq ft = $1,500 max
- **Regular method:** Actual expenses (mortgage interest/rent, utilities, insurance) × business-use percentage

Note: W-2 employees cannot deduct home office under current law (TCJA through 2025).

---

## 8. Maximize Dependent Care FSA — $5,000

If you pay for childcare while you work, contribute up to $5,000 to a Dependent Care FSA through your employer. This reduces taxable income by $5,000, worth $1,100 in tax savings at the 22% bracket.

This stacks with the Child and Dependent Care Credit for some filers.

---

## 9. Time Your Capital Gains

Realize long-term capital gains in years when your income is low — you may qualify for the **0% long-term capital gains rate** if your taxable income is under $48,350 (single) or $96,700 (MFJ) in 2025.

Retiring, taking a sabbatical, or starting a business? That could be your year for tax-free gain realization.

---

## 10. Claim All Available Credits

Credits reduce tax dollar-for-dollar — more powerful than deductions.

| Credit | Maximum | Who Qualifies |
|--------|---------|---------------|
| Child Tax Credit | $2,000/child | Income under $200K single |
| Child & Dependent Care | $2,100 (1 child) | Working parents with childcare costs |
| American Opportunity | $2,500 | First 4 years of college |
| Lifetime Learning | $2,000 | Any education |
| Saver's Credit | $1,000/$2,000 | Low-to-moderate income, retirement contributions |
| EV Tax Credit | $7,500 | Qualifying electric vehicle purchase |

---

## Action Plan: What to Do Now

1. Check if you are on track to max your 401(k) — adjust paycheck contribution
2. Open an HSA if you have an HDHP
3. Review your investment portfolio for tax-loss harvesting opportunities before year end
4. If self-employed: calculate your SEP-IRA/Solo 401(k) contribution for 2025
5. Check if you qualify for any credits you may be missing

Use our [Federal Income Tax Calculator](/tools/us-federal-income-tax-calculator/) to estimate your 2025 bill and see how each strategy affects your bottom line.
''',
    },
    {
        'slug': 'fica-tax-2025-social-security-medicare-explained',
        'title': 'FICA Tax 2025: Social Security and Medicare Tax Explained',
        'category': 'us-income-tax',
        'market': 'us',
        'fy_applicable': '2025',
        'is_featured': False,
        'reading_time': 5,
        'tags': 'FICA tax 2025, social security tax, Medicare tax, payroll tax',
        'excerpt': ('FICA tax is 7.65% for W-2 employees — split between Social Security (6.2%) '
                    'and Medicare (1.45%). Your employer matches it. Self-employed people pay '
                    'the full 15.3% as SE tax. Here is exactly how it works in 2025.'),
        'meta_title': 'FICA Tax 2025: Social Security (6.2%) + Medicare (1.45%) Explained',
        'meta_description': ('FICA tax 2025: employees pay 7.65% (SS 6.2% + Medicare 1.45%), '
                             'employers match it. SS wage base is $176,100 in 2025. '
                             'Self-employed pay 15.3% SE tax. Full explanation with examples.'),
        'body': '''## What Is FICA Tax?

FICA stands for **Federal Insurance Contributions Act**. It funds two programs: Social Security and Medicare. It is separate from federal income tax and applies to wages (W-2 income) and self-employment income.

---

## 2025 FICA Rates

| Tax | Employee Rate | Employer Rate | Self-Employed |
|-----|--------------|--------------|---------------|
| Social Security | 6.2% | 6.2% | 12.4% |
| Medicare | 1.45% | 1.45% | 2.9% |
| **Total** | **7.65%** | **7.65%** | **15.3%** |

---

## Social Security Wage Base 2025

Social Security tax only applies to wages up to the **wage base**: **$176,100** in 2025 (up from $168,600 in 2024).

Once you earn $176,100 from wages, you stop paying the 6.2% SS portion for the rest of the year. Your employer also stops paying their 6.2% match.

**Maximum Social Security tax paid by employee in 2025:** $176,100 × 6.2% = **$10,918**

Medicare tax has **no wage cap** — you pay 1.45% on all wages.

---

## Additional Medicare Tax (0.9%)

High earners pay an extra **0.9% Medicare tax** on wages above:
- **$200,000** for single filers
- **$250,000** for married filing jointly
- **$125,000** for married filing separately

This is withheld by your employer once your wages exceed $200,000, regardless of filing status. You true up at tax time — if you are MFJ with $150K + $150K = $300K combined, you owe 0.9% on $50,000 = $450.

---

## Example: W-2 Employee, $85,000 Salary

| Tax | Calculation | Amount |
|-----|------------|--------|
| Social Security (employee) | $85,000 × 6.2% | $5,270 |
| Medicare (employee) | $85,000 × 1.45% | $1,232 |
| **Total FICA withheld** | | **$6,502** |
| Social Security (employer) | $85,000 × 6.2% | $5,270 |
| Medicare (employer) | $85,000 × 1.45% | $1,232 |
| **Total FICA cost** | | **$13,004** |

The employer pays $6,502 that you never see — this is part of your total compensation cost.

---

## FICA for Self-Employed: SE Tax

Self-employed people pay **both** shares as SE (self-employment) tax = **15.3%** on 92.35% of net profit (the 92.35% factor approximates the employer deduction).

However, you can deduct **50% of SE tax** from your gross income — partially compensating for paying both shares.

---

## How FICA Appears on Your Pay Stub

Look for these line items:
- **Fed OASDI/EE** or **SS Tax** = Social Security (6.2%)
- **Fed MED/EE** or **Medicare** = Medicare (1.45%)
- If applicable: **Add Medicare** = Additional Medicare (0.9%)

---

See your full FICA calculation with our [Paycheck Calculator](/tools/us-paycheck-calculator/) — shows exact SS, Medicare, and take-home per pay period.
''',
    },
    {
        'slug': 'tax-refund-2025-how-to-maximize',
        'title': 'Tax Refund 2025: Will You Get One — And How to Make It Bigger',
        'category': 'us-tax-guides',
        'market': 'us',
        'fy_applicable': '2025',
        'is_featured': False,
        'reading_time': 6,
        'tags': 'tax refund 2025, how to get bigger refund, IRS refund, W-4 withholding',
        'excerpt': ('Whether you get a refund — and how big — depends on how much was withheld '
                    'from your paycheck vs your actual tax liability. Refund = overwithholding, '
                    'not a bonus. Here is how to estimate yours and whether you should aim for '
                    'a refund at all.'),
        'meta_title': 'Tax Refund 2025: How to Estimate It and Make It Bigger',
        'meta_description': ('Estimate your 2025 tax refund: tax owed minus withholding. '
                             'Increase your refund with credits, deductions, and W-4 adjustments. '
                             'Or stop overwithholding and invest the money yourself.'),
        'body': '''## What Is a Tax Refund (Really)?

A tax refund is the IRS returning money you *overpaid* throughout the year. When your employer withholds taxes from each paycheck, they estimate your annual liability. If they withheld too much, you get a refund.

**Refund = Taxes Withheld – Taxes Actually Owed**

A large refund is not a windfall — you gave the government an interest-free loan. Many financial advisors suggest aiming for near-zero refund and investing the difference.

That said, many people prefer the forced savings aspect of overwithholding. Whatever works for your financial behavior is fine.

---

## How to Calculate Your Estimated 2025 Refund

1. Find your total W-2 federal withholding (Box 2 on all W-2s)
2. Calculate your actual federal tax liability ([use our calculator](/tools/us-federal-income-tax-calculator/))
3. Refund = Withholding – Tax Liability (if positive)
4. Amount Owed = Tax Liability – Withholding (if negative)

**Example:**
- W-2 income: $72,000
- Federal withheld: $9,200
- Standard deduction (single): -$15,000
- Taxable income: $57,000
- Federal income tax: ~$8,394
- **Estimated refund: $9,200 – $8,394 = $806**

---

## 5 Ways to Get a Larger Refund (or Owe Less)

### 1. Claim the Child Tax Credit
Up to **$2,000 per qualifying child** under age 17. Phases out above $200,000 (single) or $400,000 (MFJ). This is a **credit** — reduces tax dollar-for-dollar.

### 2. Contribute to a Traditional IRA by April 15
You can make 2025 IRA contributions up until **April 15, 2026**. Contributing reduces your taxable income, which reduces your tax bill and potentially increases your refund.

### 3. Claim the Earned Income Tax Credit (EITC)
One of the most valuable credits for low-to-moderate income earners. Up to $7,830 for three+ children in 2025. Fully refundable — you get it even if you owe no tax.

### 4. Claim Education Credits
- **American Opportunity Credit:** Up to $2,500 for first 4 years of college (40% refundable)
- **Lifetime Learning Credit:** Up to $2,000 for any higher education

### 5. Deduct Self-Employment Expenses
If you have any freelance income, every legitimate business expense reduces your net profit and tax bill.

---

## Should You Aim for a Big Refund?

**Arguments for overwithholding (bigger refund):**
- Forces savings behavior
- Avoids underpayment penalty risk
- Simple peace of mind

**Arguments against:**
- You lose the time value of money (the IRS pays no interest on refunds)
- At 5% investment return, $5,000 overwithholding costs you $250/year in opportunity cost
- Risk of money sitting in IRS hands during financial emergencies

**The math:** If you typically get a $3,000 refund, adjusting your W-4 to withhold $250 less per month would put that money in your hands throughout the year. Invested at 5%, it grows to approximately $3,150 — $150 more than the refund.

---

## How to Adjust Your Withholding (W-4)

If you consistently get a large refund or owe a lot, submit a new **Form W-4** to your employer:

1. Go to [IRS Tax Withholding Estimator](https://www.irs.gov/individuals/tax-withholding-estimator)
2. Enter your income, deductions, and credits
3. It recommends the correct withholding amount
4. Update your W-4 with HR

---

Use our [Tax Refund Estimator](/tools/us-tax-refund-estimator/) to see your 2025 refund or amount owed in seconds.
''',
    },
    {
        'slug': 'w4-form-guide-2025',
        'title': 'How to Fill Out Form W-4 in 2025: Step-by-Step Guide',
        'category': 'us-tax-guides',
        'market': 'us',
        'fy_applicable': '2025',
        'is_featured': False,
        'reading_time': 6,
        'tags': 'how to fill out W-4 2025, W-4 form, withholding allowances, paycheck withholding',
        'excerpt': ('Form W-4 tells your employer how much federal tax to withhold from each '
                    'paycheck. Getting it right means no big surprise tax bill — and no '
                    'over-lending money to the IRS. Here is how to fill it out correctly '
                    'for 2025.'),
        'meta_title': 'How to Fill Out Form W-4 in 2025: Step-by-Step Guide',
        'meta_description': ('Step-by-step guide to filling out Form W-4 in 2025. '
                             'Single vs married, multiple jobs, dependents, and extra withholding. '
                             'Get your withholding right and avoid an IRS surprise.'),
        'body': '''## What Is Form W-4?

Form W-4 (Employee Withholding Certificate) tells your employer how much federal income tax to withhold from each paycheck. You complete it when you start a job and can update it anytime.

The current W-4 (redesigned in 2020) no longer uses "allowances." Instead, it uses dollar amounts.

---

## The 5 Steps of Form W-4

### Step 1: Personal Information (Required)
Enter your name, address, SSN, and filing status:
- **Single or Married filing separately**
- **Married filing jointly or Qualifying surviving spouse**
- **Head of household**

### Step 2: Multiple Jobs or Spouse Works (Complete If Applicable)
If you have more than one job, or you are married and your spouse also works, you need extra withholding. Options:

**Option A:** Use the IRS Tax Withholding Estimator at irs.gov and enter the result in Step 4(c)

**Option B:** Check the box in Step 2(c) — your employer will withhold as if you are single with no adjustments (overwitholds slightly, guarantees no underpayment)

**Option C:** Use the Multiple Jobs Worksheet on Page 3 of the form

**Most accurate:** Option A (IRS estimator)

### Step 3: Claim Dependents (Reduces Withholding)
If your income is under $200,000 (single) or $400,000 (MFJ), you can reduce withholding by claiming the Child Tax Credit:
- $2,000 × number of children under 17
- $500 × number of other dependents

**Example:** 2 children under 17 → Enter $4,000 on line 3.

### Step 4: Other Adjustments (Optional)
**4(a) Other income not from jobs** — Investment income, retirement distributions, freelance income. Adding it here increases withholding to cover the tax.

**4(b) Deductions** — If you plan to itemize or have other deductions exceeding the standard deduction, enter the excess amount. Reduces withholding.

**4(c) Extra withholding** — A flat dollar amount to withhold *extra* per paycheck. Useful if you have side income, a spouse works, or you want a cushion.

### Step 5: Sign and Date (Required)
---

## Common W-4 Scenarios

### Single, one job, no dependents
Fill out Step 1 only. Simple. Withholding will approximate your actual tax.

### Married, both spouses work
Both spouses should fill out Step 2. The easiest approach: check the Step 2(c) box on both W-4s. You may overwithhold slightly but it prevents underpayment.

### Freelance income on the side
Add your expected freelance income in Step 4(a). This increases withholding to cover the income tax on that income. (Does not cover SE tax — pay quarterly estimated taxes separately.)

### You always owe a big bill
You are underwithholding. Add extra withholding in Step 4(c). Start with $50–$100/paycheck and adjust.

### You always get a huge refund
You are overwithholding. Reduce withholding by adding dependents (if applicable) or use the IRS estimator to find the right amount.

---

## When to Update Your W-4

Update your W-4 whenever your situation changes:
- Marriage or divorce
- Birth or adoption of a child
- New job or significant income change
- You start a side business
- You consistently owe a lot or get a large refund

---

See how withholding affects your take-home with our [Paycheck Calculator](/tools/us-paycheck-calculator/).
''',
    },
]


class Command(BaseCommand):
    help = 'Seed 10 US tax blog articles (Tax Year 2025)'

    def handle(self, *args, **options):
        # Create US categories
        cats = {}
        for cat_data in US_CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name'], 'description': cat_data['description']},
            )
            cats[cat_data['slug']] = cat
            self.stdout.write(f'  Category {"created" if created else "exists"}: {cat.name}')

        # Create US author
        author, created = Author.objects.get_or_create(
            name=US_AUTHOR['name'],
            defaults={
                'title': US_AUTHOR['title'],
                'bio': US_AUTHOR['bio'],
                'is_ca': US_AUTHOR['is_ca'],
            }
        )
        self.stdout.write(f'  Author {"created" if created else "exists"}: {author.name}')

        # Create articles
        created_count = 0
        updated_count = 0
        for a in ARTICLES:
            cat = cats.get(a['category'])
            defaults = {
                'title': a['title'],
                'market': a['market'],
                'author': author,
                'category': cat,
                'tags': a['tags'],
                'body': a['body'],
                'excerpt': a['excerpt'],
                'fy_applicable': a['fy_applicable'],
                'is_featured': a['is_featured'],
                'is_published': True,
                'published_at': timezone.now(),
                'reading_time': a['reading_time'],
                'meta_title': a['meta_title'],
                'meta_description': a['meta_description'],
            }
            obj, is_new = Article.objects.update_or_create(slug=a['slug'], defaults=defaults)
            if is_new:
                created_count += 1
            else:
                updated_count += 1
            self.stdout.write(f'  Article {"created" if is_new else "updated"}: {obj.title[:60]}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {created_count} created, {updated_count} updated. '
            f'Total US articles: {created_count + updated_count}'
        ))
