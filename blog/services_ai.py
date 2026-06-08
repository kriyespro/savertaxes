import requests
from decimal import Decimal
from decouple import config

OPENROUTER_API_KEY = config('OPENROUTER_API_KEY', default='')
OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'
DEFAULT_MODEL          = config('OPENROUTER_MODEL', default='google/gemini-2.5-flash')
DEFAULT_KEYWORD_MODEL   = 'google/gemini-2.5-flash'       # recommended
DEFAULT_ARTICLE_MODEL   = 'anthropic/claude-sonnet-4.6'   # recommended
DEFAULT_BULK_MODEL      = 'google/gemini-2.5-flash'       # recommended
DEFAULT_HUMANIZE_MODEL  = 'google/gemini-2.5-flash'       # cheap + good at style edits

# (input_per_1M_usd, output_per_1M_usd)
MODEL_PRICING = {
    'anthropic/claude-sonnet-4.6':       (3.00,  15.00),
    'anthropic/claude-sonnet-4.5':       (3.00,  15.00),
    'anthropic/claude-haiku-4.5':        (1.00,   5.00),
    'anthropic/claude-opus-4.8':         (5.00,  25.00),
    'google/gemini-2.5-pro':             (1.25,  10.00),
    'google/gemini-2.5-flash':           (0.30,   2.50),
    'google/gemini-2.5-flash-lite':      (0.10,   0.40),
    'google/gemini-3.1-flash-lite':      (0.25,   1.00),
    'google/gemini-3.5-flash':           (1.50,   6.00),
    'deepseek/deepseek-chat-v3-0324':    (0.20,   0.80),
    'deepseek/deepseek-v3.1-terminus':   (0.27,   1.10),
    'deepseek/deepseek-v4-flash':        (0.10,   0.40),
    'deepseek/deepseek-r1-0528':         (0.50,   2.19),
    'openai/gpt-4o':                     (2.50,  10.00),
    'openai/gpt-4o-mini':                (0.15,   0.60),
}


def calc_cost(model, prompt_tokens, completion_tokens):
    input_rate, output_rate = MODEL_PRICING.get(model, (0.0, 0.0))
    cost = (prompt_tokens * input_rate + completion_tokens * output_rate) / 1_000_000
    return Decimal(str(round(cost, 6)))


KEYWORD_SYSTEM_PROMPT = """You are a Senior SEO Strategist & Semantic Search Specialist with 15+ years of experience. You specialise in finding LOW COMPETITION opportunities that new/mid-authority sites can rank for quickly.

OBJECTIVE:
1. Find 25-30 LOW COMPETITION long-tail keywords (target KD 0-30) around the seed keyword.
2. Prioritise: specific questions, how-to variants, vs/comparison, calculator-intent, guide-intent.
3. Avoid broad head terms (KD 60+) — focus on long-tail where a new site can win page 1 in 3-6 months.
4. Group keywords into topic clusters (e.g. "calculator intent", "how-to guides", "comparison", "deductions").
5. Estimate realistic 2026 SEO metrics for the specified market.

PROCESS:
1. Analyze Intent: Informational, Navigational, Commercial, or Transactional.
2. Deep expansion into long-tail variations — specific user questions, niche sub-topics, local/contextual variants.
3. Metric Estimation:
    - KD (0-100): TARGET 0-30. Include up to 5 medium (31-50) if very high-value.
    - Monthly Volume: realistic estimate for specified market.
    - CPC: average cost-per-click in market currency (INR for india, USD for us).
    - Priority: High (KD<20 + vol>500), Medium (KD<30 + vol>200), Low (rest).

OUTPUT FORMAT (STRICT — output ONLY the markdown table, zero intro text, zero commentary):
| Keyword | Cluster | Intent | Search Volume (Est) | KD (%) | CPC | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"""

ARTICLE_SYSTEM_PROMPT = """You are an elite Content Strategist and SEO Copywriter with 15 years of experience in high-converting, organic growth marketing.

WRITING STYLE: "High-Perplexity, High-Burstiness" — diverse vocabulary, varied sentence structures (mix short punchy sentences with longer analytical ones), 100% human-like feel. Never sound like AI.

PHASE 1 — STRATEGIC RESEARCH (internal, do not output):
- Identify the Primary Keyword and 5 LSI keywords to weave naturally into the article.
- Determine Search Intent (Informational / Transactional / Navigational).
- Identify the Value Gap — what other articles on this topic miss — and fill it.

PHASE 2 — WRITING RULES (Anti-AI Protocol):
- Tone: Professional yet conversational. Use second-person ("you") or first-person plural ("we").
- NEVER write: "In the rapidly evolving landscape", "In today's world", "In conclusion", "It's worth noting", "Dive into".
- Hook: Start with a Pattern Interrupt — a surprising stat, a bold counter-intuitive claim, or a sharp question.
- Structure:
  * H2 and H3 hierarchy (NOT H1 — title stored separately)
  * Paragraphs max 2-3 sentences
  * Bullet lists and **bold text** for skimmability
  * At least one data table with real numbers
- Length: Minimum 1200 words. Include real calculations and examples.
- Links: Suggest 2 external high-authority sources (in [brackets]) + 2 internal link placeholders as [INTERNAL: anchor text].
- End with a clear, specific call-to-action (not generic "consult a professional").

PHASE 3 — EEAT COMPLIANCE:
- Cite specific rules, sections, government sources where relevant (CBDT, IRS, etc.)
- Include "Last updated: FY 2025-26" or "Tax Year 2025" note.
- Add disclaimer at end: "This article is for informational purposes only and does not constitute tax advice."

RETURN EXACTLY THIS STRUCTURE (no extra --- separators inside sections):
---META---
TITLE_TAG: [50-60 chars, include primary keyword]
META_DESC: [max 155 chars, include primary keyword, end with a benefit]
SLUG: [url-friendly-slug-no-spaces]
EXCERPT: [2-3 sentences, max 350 chars, hook the reader]
READING_TIME: [number in minutes]
TAGS: [comma-separated, max 8 tags]
---ARTICLE---
[Full article in Markdown. H2 first — NOT H1.]
---FAQ---
**Q: [People Also Ask style question]?**
A: [2-4 sentence answer, specific and actionable]

[repeat for 4-5 questions]"""


def _call_openrouter(messages, model=DEFAULT_MODEL, temperature=0.7):
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not set in .env")

    resp = requests.post(
        OPENROUTER_URL,
        json={'model': model, 'messages': messages, 'temperature': temperature},
        headers={
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'HTTP-Referer': 'https://taxessaver.com',
            'X-Title': 'TaxesSaver SEO Tools',
        },
        timeout=180,
    )
    resp.raise_for_status()
    data = resp.json()
    content = data['choices'][0]['message']['content']
    usage = data.get('usage', {})
    prompt_tokens     = usage.get('prompt_tokens', 0)
    completion_tokens = usage.get('completion_tokens', 0)
    cost = calc_cost(model, prompt_tokens, completion_tokens)
    return content, prompt_tokens, completion_tokens, cost


def research_keywords(seed_keyword, market='india', model=DEFAULT_MODEL):
    market_ctx = (
        'India — INR currency, Indian tax/finance, CBDT, FY 2025-26'
        if market == 'india'
        else 'USA — USD currency, US tax/finance, IRS, Tax Year 2025'
    )
    user_msg = (
        f"Seed Keyword: {seed_keyword}\n"
        f"Market: {market} ({market_ctx})\n\n"
        "Generate 25-30 LOW COMPETITION keywords (KD 0-30). Output ONLY the markdown table."
    )
    return _call_openrouter(
        [
            {'role': 'system', 'content': KEYWORD_SYSTEM_PROMPT},
            {'role': 'user', 'content': user_msg},
        ],
        model=model,
        temperature=0.5,
    )


def generate_article(keyword, market='india', context='', model=DEFAULT_MODEL):
    market_ctx = (
        'Indian tax system, INR currency, CBDT rules, FY 2025-26, Indian audience'
        if market == 'india'
        else 'US tax system, USD currency, IRS rules, Tax Year 2025, American audience'
    )
    user_msg = (
        f"Topic/Primary Keyword: {keyword}\n"
        f"Market: {market} ({market_ctx})\n"
        f"{f'Additional context: {context}' if context else ''}\n\n"
        "Write the complete SEO article following the exact output structure."
    )
    return _call_openrouter(
        [
            {'role': 'system', 'content': ARTICLE_SYSTEM_PROMPT},
            {'role': 'user', 'content': user_msg},
        ],
        model=model,
        temperature=0.75,
    )


def parse_keyword_table(raw_text):
    """Parse AI markdown table (with optional Cluster column) into list of dicts."""
    rows = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line.startswith('|') or line.startswith('| :') or 'Keyword' in line[:20]:
            continue
        cols = [c.strip() for c in line.strip('|').split('|')]
        if len(cols) < 6:
            continue
        # Support both 6-col (no cluster) and 7-col (with cluster) tables
        if len(cols) >= 7:
            keyword, cluster, intent, volume, kd_raw, cpc, priority = cols[:7]
        else:
            keyword, intent, volume, kd_raw, cpc, priority = cols[:6]
            cluster = ''
        try:
            kd = int(''.join(c for c in kd_raw if c.isdigit()) or '0')
        except ValueError:
            kd = 0
        rows.append({
            'keyword':      keyword.strip(),
            'cluster':      cluster.strip(),
            'intent':       intent.strip(),
            'search_volume': volume.strip(),
            'kd':           kd,
            'cpc':          cpc.strip(),
            'priority':     priority.strip(),
        })
    return rows


PIPELINE_RESEARCH_PROMPT = """# KSV Framework — PHASE 1 + PHASE 2: Research & Content Strategy

You are a senior content strategist and subject matter researcher. Your goal is to be useful, accurate, and trustworthy — not creative. If accuracy conflicts with creativity, choose accuracy.

Do NOT write the article. Produce a research brief only.

## PHASE 1 — SEARCH INTENT ANALYSIS

Identify:
1. Primary keyword
2. Secondary keywords (5-8)
3. Long-tail keyword variations (5-8)
4. LSI keywords (6-8 semantic/related terms)
5. Search intent (Informational / Commercial / Comparison / Guide / Tutorial)
6. User pain points (what problem are they trying to solve?)
7. People Also Ask questions (8 real questions users search)
8. VALUE GAP REPORT: "What useful information is missing from most competing pages on this topic?"

## PHASE 2 — CONTENT STRATEGY

Identify questions at all three levels:
- Beginner questions (someone new to this topic)
- Intermediate questions (someone who knows basics)
- Advanced questions (someone optimising or in edge-case scenarios)

Then produce:

## RESEARCH OUTPUT FORMAT

### Primary Keyword
[exact keyword]

### Search Intent
[intent type + one-line explanation]

### Keywords
**Secondary:** [list]
**Long-tail:** [list]
**LSI:** [list]

### User Pain Points
[bullet list — what problem brings someone to this article?]

### People Also Ask (8 questions)
[numbered list]

### Value Gap Report
[2-3 sentences: what most competing pages miss or get wrong on this topic]

### Beginner / Intermediate / Advanced Questions
**Beginner:** [3 questions]
**Intermediate:** [3 questions]
**Advanced:** [3 questions]

### Key Facts & Data Points
[bullet list — specific numbers, limits, rates, dates. No vague statements. Flag anything uncertain with (?)]

### Tax Rules & Sections to Cover
[exact section numbers, sub-sections, limits, thresholds, deadlines]

### Suggested Content Outline
[H2 and H3 hierarchy — full article structure that covers beginner → advanced]

### Authoritative Sources to Cite
[2 government or high-authority sources]"""

PIPELINE_DRAFT_PROMPT = """# KSV Framework — PHASE 4 + PHASE 5: Writing Style & SEO Structure

You are an experienced SEO content writer. Write a complete first-draft article using the research brief provided.

## PHASE 4 — WRITING STYLE RULES

Use:
- Clear language (avoid jargon unless legally required)
- Short paragraphs (max 3 sentences)
- Natural sentence variation (mix short and longer sentences)
- Professional tone — write like an experienced professional explaining something important

STRICTLY AVOID these words and phrases:
- "In today's fast-paced world" / "In today's digital age"
- "In conclusion"
- "Unlocking" / "Decoding" / "Revolutionizing"
- "Game-changing" / "Game-changer"
- "Seamless" / "Seamlessly"
- "Delve into" / "Dive into"
- "Here's the truth" / "The reality is"
- "Leverage" / "Supercharge" / "Empower"
- Any high-drama marketing language

## PHASE 5 — SEO STRUCTURE

Build the article with:
- H1 (title only — do not repeat, stored separately)
- Introduction (hook — pattern interrupt, surprising stat, or sharp question)
- H2 sections covering beginner → intermediate → advanced questions from the brief
- H3 sub-sections where needed
- At least 1 data table with real numbers from the research
- Bullet lists for skimmability
- Real examples with specific numbers
- Action Steps section near the end
- FAQ section (use the PAA questions from the research brief)

## PHASE 6 — LINKS

- Add 2-5 internal link placeholders: [INTERNAL: relevant article topic]
- Note 2 places where official external sources should be linked (as [EXTERNAL: source name/url])

OUTPUT EXACTLY THIS FORMAT (no extra separators):
---META---
TITLE_TAG: [50-60 chars, include primary keyword]
META_DESC: [max 155 chars, include primary keyword + benefit]
SLUG: [url-friendly-slug]
EXCERPT: [2-3 sentences, max 350 chars]
READING_TIME: [minutes]
TAGS: [comma-separated, max 8]
---ARTICLE---
[Full draft in Markdown. Start with H2 — NOT H1.]
---FAQ---
**Q: [PAA-style question from research]?**
A: [2-4 sentence answer]

[repeat 5-6 times]"""

PIPELINE_HUMANIZE_PROMPT = """# KSV Framework — PHASE 3 (Continued): Practitioner Insights + Humanization

You are a senior tax practitioner and plain-language editor. Your goal is NOT to sound human — your goal is to be useful, accurate, and easy to read.

Apply ALL of the following:

## 1. PRACTITIONER INSIGHTS (add exactly 2)

Insert observations only a real practitioner would know.
Format: short paragraph starting with "In practice, ..." or "From experience, ..." or "What many taxpayers don't realise is..."

Examples of practitioner insights:
- Filing edge cases (e.g. what happens when a deadline falls on a Sunday)
- How tax officers actually process claims
- A timing nuance that saves money
- A frequently misunderstood rule

Place: one in the first half, one in the second half.

## 2. COMMON MISTAKE BOX (add exactly 1)

Format as a markdown blockquote:

> ⚠️ **Common Mistake:** [describe one specific mistake real taxpayers make + consequence]

Example:
> ⚠️ **Common Mistake:** Many salaried employees forget to submit rent receipts above ₹1 lakh to their employer before January. The result: HRA goes unclaimed and TDS is deducted on the full salary — a loss that cannot be recovered until the next ITR filing.

## 3. REAL-WORLD SCENARIO (add exactly 1)

Add a concrete narrative example with:
- Indian name: Arjun, Priya, Ramesh, Kavitha, Suresh (for India market)
- US name: Sarah, Mike, James, Lisa, David (for US market)
- Specific numbers: income, deduction amounts, tax saved/owed
- 2-4 sentences as a narrative paragraph (not a table)
- Place after the first major comparison or calculation

Example:
"Priya is a 32-year-old software engineer in Bangalore earning ₹14 lakh annually. She contributes ₹1.5 lakh to ELSS, pays ₹18,000 for a family health insurance policy, and her employer contributes ₹84,000 to NPS under Section 80CCD(2). Under the old regime, her taxable income drops to ₹9.93 lakh — saving her ₹41,600 in tax compared to the new regime."

## 4. STRIP MARKETING LANGUAGE

Remove or replace every instance of:
unlock, supercharge, game-changer, game-changing, seamlessly, seamless, robust, leverage, cutting-edge, skyrocket, empower, holistic, best-in-class, revolutionize, transformative

Replace with plain direct alternatives.

## 5. SIMPLIFY LANGUAGE

- "utilise" → "use"
- "remuneration" → "salary"
- "ascertain" → "find out" or "check"
- "subsequent" → "next"
- "endeavour" → "try"
- Keep all legally required tax terms (Section 80C, AY 2026-27, etc.)
- Break sentences longer than 30 words into two sentences

## 6. PRESERVE EVERYTHING ELSE

- All ---META--- / ---ARTICLE--- / ---FAQ--- formatting exactly
- All facts, numbers, tax rules, section references — do not alter any data
- All [INTERNAL: ...] and [EXTERNAL: ...] placeholders
- The disclaimer at the end
- Any [VERIFY: ...] flags from the previous step — keep them visible

Return the COMPLETE article in the exact same ---META--- / ---ARTICLE--- / ---FAQ--- format."""

PIPELINE_REWRITE_PROMPT = """# KSV Framework — PHASE 3 + PHASE 7 + PHASE 8: EEAT, Fact Check & Quality

You are a senior SEO editor with deep expertise in EEAT (Experience, Expertise, Authoritativeness, Trustworthiness). Your job is to transform a draft into publish-ready content that ranks and is genuinely trustworthy.

## PHASE 3 — TRUST & EEAT

Add trust signals throughout:
- Reference specific laws, sections, regulations, government sources
- Add "as of FY 2025-26" or "per CBDT guidelines" or "per IRS Publication X" where relevant
- Write with the authority of someone who has handled real cases

## PHASE 7 — FACT CHECK AUDIT (critical step)

Review EVERY:
- Percentage / tax rate
- Date / deadline
- Tax slab threshold
- Legal section number
- Deduction amount / limit
- Any statistic or figure

Rules:
- If a fact is verifiable and accurate → keep it
- If a fact seems uncertain or invented → FLAG IT with [VERIFY: reason] or remove it
- NEVER fabricate statistics or exact figures you cannot confirm
- If using approximate language, qualify it: "approximately", "typically", "in most cases"

## PHASE 8 — FINAL QUALITY CHECKLIST

Before outputting, verify:
✓ Search intent fully satisfied (beginner → advanced covered)
✓ Practical value: reader can act on this immediately
✓ Original examples included (real numbers, real scenarios)
✓ EEAT signals present throughout
✓ No unsupported statistics
✓ No filler content
✓ No AI clichés (check for: "unlock", "delve", "game-changing", "seamless", "leverage")
✓ Hook is a genuine Pattern Interrupt (not generic)
✓ CTA is specific and action-oriented
✓ Internal links present [INTERNAL: topic]
✓ External source notes present [EXTERNAL: source]
✓ Disclaimer present at end

## REWRITE OUTPUT

Return the COMPLETE article in the EXACT same ---META--- / ---ARTICLE--- / ---FAQ--- format.
Improve META fields if the draft versions are weak.
Do not change the SLUG."""


def generate_article_pipeline(keyword, market='india', context='',
                               research_model=None, draft_model=None,
                               rewrite_model=None, humanize_model=None):
    """
    4-step pipeline:
      Step 1 (research_model  / Gemini):  deep research brief
      Step 2 (draft_model     / DeepSeek): full article draft
      Step 3 (rewrite_model   / Claude):  SEO polish + rewrite
      Step 4 (humanize_model  / Gemini):  humanization layer
    Returns (content, total_prompt_tokens, total_completion_tokens, total_cost, step_log)
    """
    research_model  = research_model  or DEFAULT_KEYWORD_MODEL
    draft_model     = draft_model     or DEFAULT_BULK_MODEL
    rewrite_model   = rewrite_model   or DEFAULT_ARTICLE_MODEL
    humanize_model  = humanize_model  or DEFAULT_HUMANIZE_MODEL

    market_ctx = (
        'Indian tax system, INR currency, CBDT rules, FY 2025-26'
        if market == 'india'
        else 'US tax system, USD currency, IRS rules, Tax Year 2025'
    )

    total_prompt = total_completion = 0
    total_cost = Decimal('0')
    step_log = []

    # ── Step 1: Research ────────────────────────────────────────────────
    research_content, p, c, cost = _call_openrouter(
        messages=[
            {'role': 'system', 'content': PIPELINE_RESEARCH_PROMPT},
            {'role': 'user', 'content': (
                f"Topic: {keyword}\n"
                f"Market: {market} ({market_ctx})\n"
                f"{f'Extra context: {context}' if context else ''}\n\n"
                "Produce the complete research brief."
            )},
        ],
        model=research_model,
        temperature=0.3,
    )
    total_prompt += p; total_completion += c; total_cost += cost
    step_log.append(f"Step1 Research [{research_model}]: {p}in/{c}out = ${cost:.4f}")

    # ── Step 2: Draft ───────────────────────────────────────────────────
    draft_content, p, c, cost = _call_openrouter(
        messages=[
            {'role': 'system', 'content': PIPELINE_DRAFT_PROMPT},
            {'role': 'user', 'content': (
                f"RESEARCH BRIEF:\n{research_content}\n\n"
                f"Topic keyword: {keyword}\n"
                f"Market: {market} ({market_ctx})\n"
                "Write the complete first-draft article."
            )},
        ],
        model=draft_model,
        temperature=0.7,
    )
    total_prompt += p; total_completion += c; total_cost += cost
    step_log.append(f"Step2 Draft [{draft_model}]: {p}in/{c}out = ${cost:.4f}")

    # ── Step 3: Rewrite ─────────────────────────────────────────────────
    rewritten_content, p, c, cost = _call_openrouter(
        messages=[
            {'role': 'system', 'content': PIPELINE_REWRITE_PROMPT},
            {'role': 'user', 'content': (
                f"DRAFT TO REWRITE:\n{draft_content}\n\n"
                "Rewrite and polish the full article. Return in exact format."
            )},
        ],
        model=rewrite_model,
        temperature=0.6,
    )
    total_prompt += p; total_completion += c; total_cost += cost
    step_log.append(f"Step3 Rewrite [{rewrite_model}]: {p}in/{c}out = ${cost:.4f}")

    # ── Step 4: Humanize ────────────────────────────────────────────────
    final_content, p, c, cost = _call_openrouter(
        messages=[
            {'role': 'system', 'content': PIPELINE_HUMANIZE_PROMPT},
            {'role': 'user', 'content': (
                f"ARTICLE TO HUMANIZE:\n{rewritten_content}\n\n"
                f"Market: {market} — use {'Indian names (Arjun, Priya, Ramesh)' if market == 'india' else 'US names (Sarah, Mike, James)'}.\n"
                "Apply all humanization rules. Return in exact format."
            )},
        ],
        model=humanize_model,
        temperature=0.8,
    )
    total_prompt += p; total_completion += c; total_cost += cost
    step_log.append(f"Step4 Humanize [{humanize_model}]: {p}in/{c}out = ${cost:.4f}")

    return final_content, total_prompt, total_completion, total_cost, '\n'.join(step_log)


def parse_article_response(text):
    """Extract structured fields from AI response."""
    result = {
        'meta_title': '', 'meta_description': '', 'slug': '',
        'excerpt': '', 'reading_time': 7, 'tags': '', 'body': '',
    }
    if '---META---' not in text or '---ARTICLE---' not in text:
        result['body'] = text
        return result
    try:
        meta_raw = text.split('---META---')[1].split('---ARTICLE---')[0]
        after_article = text.split('---ARTICLE---')[1]
        article_raw, faq_raw = (
            after_article.split('---FAQ---', 1)
            if '---FAQ---' in after_article
            else (after_article, '')
        )
        for line in meta_raw.splitlines():
            line = line.strip()
            if line.startswith('TITLE_TAG:'):
                result['meta_title'] = line[len('TITLE_TAG:'):].strip()[:70]
            elif line.startswith('META_DESC:'):
                result['meta_description'] = line[len('META_DESC:'):].strip()[:165]
            elif line.startswith('SLUG:'):
                result['slug'] = line[len('SLUG:'):].strip()
            elif line.startswith('EXCERPT:'):
                result['excerpt'] = line[len('EXCERPT:'):].strip()[:400]
            elif line.startswith('READING_TIME:'):
                try:
                    result['reading_time'] = int(line[len('READING_TIME:'):].strip().split()[0])
                except (ValueError, IndexError):
                    pass
            elif line.startswith('TAGS:'):
                result['tags'] = line[len('TAGS:'):].strip()
        body = article_raw.strip()
        if faq_raw.strip():
            body += '\n\n## Frequently Asked Questions\n\n' + faq_raw.strip()
        result['body'] = body
    except Exception:
        result['body'] = text
    return result
