from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import AIGenerationLog, AIModelConfig, KeywordResearch
from blog.services_ai import research_keywords, parse_keyword_table, DEFAULT_KEYWORD_MODEL


class Command(BaseCommand):
    help = 'Research low-competition SEO keywords using OpenRouter AI and save to DB'

    def add_arguments(self, parser):
        parser.add_argument('keyword', type=str, help='Seed keyword')
        parser.add_argument('--market', default='india', choices=['india', 'us'])
        parser.add_argument('--model', default=None,
                            help='Override model (default: Keyword Research Model from AI Config)')
        parser.add_argument('--output', help='Also save raw table to this file path')

    def handle(self, *args, **options):
        seed = options['keyword']
        market = options['market']
        model = options['model'] or AIModelConfig.get().keyword_model or DEFAULT_KEYWORD_MODEL

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\nKeyword research: '{seed}' [{market.upper()}] — model: {model}\n"
        ))

        log = AIGenerationLog.objects.create(
            job_type='keyword', status='running',
            keyword=seed, market=market, model_used=model,
        )

        try:
            raw, prompt_tok, completion_tok, cost = research_keywords(seed, market=market, model=model)
        except Exception as exc:
            log.status = 'failed'
            log.error_message = str(exc)
            log.completed_at = timezone.now()
            log.save()
            raise

        rows = parse_keyword_table(raw)

        saved = 0
        skipped = 0
        for row in rows:
            if not row['keyword']:
                continue
            obj, created = KeywordResearch.objects.get_or_create(
                keyword=row['keyword'].lower(),
                defaults={
                    'seed_keyword': seed,
                    'intent': row['intent'][:30],
                    'search_volume': row['search_volume'][:30],
                    'kd': row['kd'],
                    'cpc': row['cpc'][:20],
                    'priority': row['priority'][:10],
                    'market': market,
                },
            )
            if created:
                saved += 1
            else:
                skipped += 1

        log.status = 'done'
        log.output_preview = raw[:2000]
        log.prompt_tokens = prompt_tok
        log.completion_tokens = completion_tok
        log.cost_usd = cost
        log.completed_at = timezone.now()
        log.save()

        self.stdout.write('\n' + raw + '\n')
        self.stdout.write(self.style.SUCCESS(
            f"\n✓ {saved} keywords saved, {skipped} skipped\n"
            f"  Tokens:  {prompt_tok} in + {completion_tok} out\n"
            f"  Cost:    ${cost:.4f} USD\n"
            f"  View at: /sd/blog/keywordresearch/\n"
            f"  Log ID:  {log.pk} — /sd/blog/aigenerationlog/\n"
        ))

        if options.get('output'):
            with open(options['output'], 'w', encoding='utf-8') as f:
                f.write(f"# Keyword Research: {seed}\nMarket: {market}\nModel: {model}\n\n")
                f.write(raw)
            self.stdout.write(self.style.SUCCESS(f"Raw table saved to {options['output']}"))
