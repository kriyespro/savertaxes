"""
Automation command: run the 4-step KSV pipeline for all pending keywords.

Usage:
  # Dry run — show what would be processed
  python manage.py autopublish --dry-run

  # Process all High priority keywords without articles
  python manage.py autopublish

  # Process a specific market only
  python manage.py autopublish --market india --limit 5

  # Process Medium priority too
  python manage.py autopublish --priority High Medium

  # Cron example (every day at 2am):
  # 0 2 * * * cd /path/to/project && python manage.py autopublish --limit 3 >> logs/autopublish.log 2>&1
"""
import time
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from blog.models import KeywordResearch, AIModelConfig, Article


class Command(BaseCommand):
    help = 'Auto-generate articles for pending keywords using the KSV 4-step pipeline'

    def add_arguments(self, parser):
        parser.add_argument('--market', default=None, choices=['india', 'us'],
                            help='Filter by market (default: all)')
        parser.add_argument('--priority', nargs='+', default=['High'],
                            choices=['High', 'Medium', 'Low'],
                            help='Which priority keywords to process (default: High)')
        parser.add_argument('--limit', type=int, default=None,
                            help='Max articles per run (default: articles_per_hour from AI Config)')
        parser.add_argument('--category', default=None,
                            help='Category slug to assign (e.g. income-tax)')
        parser.add_argument('--author', type=int, default=1,
                            help='Author ID to assign (default: 1)')
        parser.add_argument('--no-pipeline', action='store_true',
                            help='Use single model instead of 4-step pipeline')
        parser.add_argument('--delay', type=int, default=None,
                            help='Seconds between articles (default: auto from articles_per_hour)')
        parser.add_argument('--dry-run', action='store_true',
                            help='Show which keywords would be processed, do not generate')

    def handle(self, *args, **options):
        from blog.models import AIModelConfig
        cfg = AIModelConfig.get()

        if cfg.is_paused:
            self.stdout.write(self.style.WARNING(
                'Autopublish is PAUSED. Uncheck "Pause Autopublish" in AI Config to resume.'
            ))
            return

        # Rate: read from config, override with --limit / --delay if given
        articles_per_hour = cfg.articles_per_hour or 5
        limit  = options['limit']  if options['limit']  is not None else articles_per_hour
        # delay = time between article STARTS minus ~180s generation time, min 5s
        delay  = options['delay']  if options['delay']  is not None else max(5, (3600 // articles_per_hour) - 180)

        qs = KeywordResearch.objects.filter(
            article__isnull=True,
            priority__in=options['priority'],
        ).order_by('kd')  # easiest first

        if options['market']:
            qs = qs.filter(market=options['market'])

        total = qs.count()
        batch = list(qs[:limit])

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\n{'DRY RUN — ' if options['dry_run'] else ''}"
            f"Autopublish: {len(batch)} of {total} pending keywords\n"
            f"  Priority:        {', '.join(options['priority'])}\n"
            f"  Market:          {options['market'] or 'all'}\n"
            f"  Pipeline:        {'NO — single model' if options['no_pipeline'] else 'YES — 4-step KSV'}\n"
            f"  Articles/hour:   {articles_per_hour} (from AI Config)\n"
            f"  Limit this run:  {limit}\n"
            f"  Delay between:   {delay}s\n"
        ))

        if options['dry_run']:
            self.stdout.write('\nKeywords to process:')
            for i, kw in enumerate(batch, 1):
                self.stdout.write(f"  {i:2}. [{kw.market.upper()}] KD={kw.kd:2} {kw.keyword}")
            self.stdout.write(
                f'\n  Estimated cost (pipeline ~$0.11/article): '
                f'${len(batch) * 0.11:.2f} USD'
            )
            return

        success = 0
        failed = 0

        for i, kw in enumerate(batch, 1):
            self.stdout.write(
                f"\n[{i}/{len(batch)}] '{kw.keyword}' [{kw.market.upper()}] KD={kw.kd}"
            )
            try:
                kwargs = dict(
                    market=kw.market,
                    publish=True,
                    verbosity=0,
                )
                if options['category']:
                    kwargs['category'] = options['category']
                if options['author']:
                    kwargs['author'] = options['author']
                if not options['no_pipeline']:
                    kwargs['pipeline'] = True

                call_command('generate_article', kw.keyword, **kwargs)
                success += 1
                self.stdout.write(self.style.SUCCESS(f"  ✓ Done"))

            except Exception as exc:
                failed += 1
                self.stdout.write(self.style.ERROR(f"  ✗ Failed: {exc}"))

            if i < len(batch):
                self.stdout.write(f"  Waiting {delay}s before next article...")
                time.sleep(delay)

        self.stdout.write(self.style.SUCCESS(
            f"\n{'─'*50}\n"
            f"Done: {success} published, {failed} failed\n"
            f"Next run: {total - success} keywords still pending\n"
        ))
