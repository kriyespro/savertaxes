from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from blog.models import Article, Author, Category, AIGenerationLog, AIModelConfig, KeywordResearch
from blog.services_ai import (
    generate_article, generate_article_pipeline, parse_article_response,
    DEFAULT_ARTICLE_MODEL, DEFAULT_KEYWORD_MODEL, DEFAULT_BULK_MODEL, DEFAULT_HUMANIZE_MODEL,
)


class Command(BaseCommand):
    help = 'Generate and save an SEO article using OpenRouter AI'

    def add_arguments(self, parser):
        parser.add_argument('keyword', type=str, help='Target keyword / article topic')
        parser.add_argument('--market', default='india', choices=['india', 'us'])
        parser.add_argument('--category', help='Category slug (e.g. income-tax)')
        parser.add_argument('--author', type=int, help='Author ID')
        parser.add_argument('--model', default=None,
                            help='Single model override (ignored when --pipeline is set)')
        parser.add_argument('--pipeline', action='store_true',
                            help='Use 3-step pipeline: Gemini Research → DeepSeek Draft → Claude Rewrite')
        parser.add_argument('--research-model', default=None,
                            help='Pipeline step 1 model (default: keyword_model from AI Config)')
        parser.add_argument('--draft-model', default=None,
                            help='Pipeline step 2 model (default: bulk_model from AI Config)')
        parser.add_argument('--rewrite-model', default=None,
                            help='Pipeline step 3 model (default: article_model from AI Config)')
        parser.add_argument('--humanize-model', default=None,
                            help='Pipeline step 4 model (default: humanize_model from AI Config)')
        parser.add_argument('--context', default='', help='Extra context/instructions for the AI')
        parser.add_argument('--publish', action='store_true', help='Mark as published immediately')
        parser.add_argument('--dry-run', action='store_true', help='Print output, do not save to DB')

    def handle(self, *args, **options):
        keyword = options['keyword']
        market  = options['market']
        cfg     = AIModelConfig.get()

        if options['pipeline']:
            research_model  = options['research_model']  or cfg.keyword_model   or DEFAULT_KEYWORD_MODEL
            draft_model     = options['draft_model']     or cfg.bulk_model      or DEFAULT_BULK_MODEL
            rewrite_model   = options['rewrite_model']   or cfg.article_model   or DEFAULT_ARTICLE_MODEL
            humanize_model  = options['humanize_model']  or cfg.humanize_model  or DEFAULT_HUMANIZE_MODEL
            model_label = f'{research_model} → {draft_model} → {rewrite_model} → {humanize_model}'
        else:
            single_model = options['model'] or cfg.article_model or DEFAULT_ARTICLE_MODEL
            model_label  = single_model

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\nGenerating article: '{keyword}' [{market.upper()}]\n"
            f"  Mode:  {'PIPELINE' if options['pipeline'] else 'SINGLE'}\n"
            f"  Model: {model_label}\n"
        ))

        log = AIGenerationLog.objects.create(
            job_type='article', status='running',
            keyword=keyword, market=market, model_used=model_label,
        )

        try:
            if options['pipeline']:
                self.stdout.write('  Step 1/4 — Gemini research brief ...')
                raw, prompt_tok, completion_tok, cost, step_log = generate_article_pipeline(
                    keyword,
                    market=market,
                    context=options['context'],
                    research_model=research_model,
                    draft_model=draft_model,
                    rewrite_model=rewrite_model,
                    humanize_model=humanize_model,
                )
                self.stdout.write(self.style.SUCCESS('  ✓ All 4 steps complete'))
                for line in step_log.split('\n'):
                    self.stdout.write(f'    {line}')
            else:
                raw, prompt_tok, completion_tok, cost = generate_article(
                    keyword, market=market,
                    context=options['context'], model=single_model,
                )
                step_log = ''

            fields = parse_article_response(raw)

        except Exception as exc:
            log.status = 'failed'
            log.error_message = str(exc)
            log.completed_at = timezone.now()
            log.save()
            raise

        if options['dry_run']:
            log.status = 'done'
            log.output_preview = fields['body'][:2000]
            log.prompt_tokens     = prompt_tok
            log.completion_tokens = completion_tok
            log.cost_usd          = cost
            log.completed_at      = timezone.now()
            log.save()
            self._print_preview(fields, prompt_tok, completion_tok, cost, step_log)
            self.stdout.write(f"\nDry-run log ID: {log.pk}")
            return

        author   = self._get_author(options.get('author'))
        category = self._get_category(options.get('category'))
        slug  = self._unique_slug(fields['slug'] or slugify(keyword))
        title = fields['meta_title'] or keyword.title()

        article = Article.objects.create(
            title=title, slug=slug, market=market,
            author=author, category=category,
            body=fields['body'],
            excerpt=fields['excerpt'] or fields['body'][:300],
            meta_title=fields['meta_title'][:70] if fields['meta_title'] else title[:70],
            meta_description=fields['meta_description'][:165],
            tags=fields['tags'],
            reading_time=fields['reading_time'],
            is_published=options['publish'],
            published_at=timezone.now() if options['publish'] else None,
            fy_applicable='2025-26' if market == 'india' else '2025',
        )

        log.status = 'done'
        log.article = article
        log.output_preview = fields['body'][:2000]
        log.prompt_tokens     = prompt_tok
        log.completion_tokens = completion_tok
        log.cost_usd          = cost
        log.completed_at      = timezone.now()
        if step_log:
            log.error_message = ''  # reuse field to store step breakdown (no error)
            # store step_log in output_preview prefix
            log.output_preview = f'PIPELINE STEPS:\n{step_log}\n\n---\n{fields["body"][:1800]}'
        log.save()

        KeywordResearch.objects.filter(
            keyword__iexact=keyword, market=market, article__isnull=True
        ).update(article=article)

        self.stdout.write(self.style.SUCCESS(
            f"\n✓ Article saved (ID={article.pk})\n"
            f"  Title:     {article.title}\n"
            f"  Slug:      {article.slug}\n"
            f"  Published: {article.is_published}\n"
            f"  URL:       /blog/{article.slug}/\n"
            f"  Tokens:    {prompt_tok:,} in + {completion_tok:,} out\n"
            f"  Cost:      ${cost:.4f} USD\n"
            f"  Log ID:    {log.pk} — /sd/blog/aigenerationlog/\n"
        ))

    def _print_preview(self, fields, prompt_tok, completion_tok, cost, step_log):
        self.stdout.write('\n--- DRY RUN PREVIEW ---')
        self.stdout.write(f"TITLE:        {fields['meta_title']}")
        self.stdout.write(f"SLUG:         {fields['slug']}")
        self.stdout.write(f"META DESC:    {fields['meta_description']}")
        self.stdout.write(f"READING TIME: {fields['reading_time']} min")
        self.stdout.write(f"TAGS:         {fields['tags']}")
        self.stdout.write(f"TOKENS:       {prompt_tok:,} in / {completion_tok:,} out")
        self.stdout.write(f"COST:         ${cost:.4f} USD")
        if step_log:
            self.stdout.write('\n--- PIPELINE BREAKDOWN ---')
            for line in step_log.split('\n'):
                self.stdout.write(f"  {line}")
        self.stdout.write('\n--- BODY PREVIEW (500 chars) ---')
        self.stdout.write(fields['body'][:500] + '...\n')

    def _get_author(self, author_id):
        if not author_id:
            return None
        try:
            return Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            self.stderr.write(f"Author {author_id} not found")
            return None

    def _get_category(self, slug):
        if not slug:
            return None
        cat = Category.objects.filter(slug=slug).first()
        if not cat:
            self.stderr.write(f"Category '{slug}' not found")
        return cat

    def _unique_slug(self, base):
        slug = base
        counter = 1
        while Article.objects.filter(slug=slug).exists():
            slug = f"{base}-{counter}"
            counter += 1
        return slug
