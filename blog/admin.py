from decimal import Decimal
from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from .models import (
    Article, Category, Author,
    AIGenerationLog, AIModelConfig, KeywordResearch,
)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'market', 'category', 'author', 'is_published', 'published_at', 'reading_time']
    list_filter = ['is_published', 'market', 'category', 'fy_applicable']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['title', 'slug', 'tags']
    filter_horizontal = ['related_tools']
    date_hierarchy = 'published_at'
    readonly_fields = ['updated_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'is_ca']


# ── AI Model Config (singleton) ──────────────────────────────────────────────

@admin.register(AIModelConfig)
class AIModelConfigAdmin(admin.ModelAdmin):
    fields = ['is_paused', 'articles_per_hour', 'keyword_model', 'article_model', 'bulk_model', 'humanize_model']
    readonly_fields = []

    def has_add_permission(self, request):
        return not AIModelConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = AIModelConfig.objects.get_or_create(pk=1)
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        return HttpResponseRedirect(
            reverse('admin:blog_aimodelconfig_change', args=[obj.pk])
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'AI Model Configuration'
        obj = AIModelConfig.objects.filter(pk=object_id).first()
        if obj and obj.is_paused:
            extra_context['subtitle'] = (
                '⏸ AUTOPUBLISH IS PAUSED — uncheck "Pause Autopublish" and save to resume.'
            )
        else:
            extra_context['subtitle'] = (
                'Select AI models and autopublish rate. '
                'Changes apply immediately to the next run.'
            )
        return super().change_view(request, object_id, form_url, extra_context)


# ── Keyword Research ──────────────────────────────────────────────────────────

class HasArticleFilter(admin.SimpleListFilter):
    title = 'Blog Post Status'
    parameter_name = 'has_article'

    def lookups(self, request, model_admin):
        return [('yes', 'Article Created'), ('no', 'No Article Yet')]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(article__isnull=False)
        if self.value() == 'no':
            return queryset.filter(article__isnull=True)
        return queryset


class KDFilter(admin.SimpleListFilter):
    title = 'Difficulty'
    parameter_name = 'kd_range'

    def lookups(self, request, model_admin):
        return [('easy', 'Easy (0-30)'), ('medium', 'Medium (31-60)'), ('hard', 'Hard (61+)')]

    def queryset(self, request, queryset):
        if self.value() == 'easy':
            return queryset.filter(kd__lte=30)
        if self.value() == 'medium':
            return queryset.filter(kd__gt=30, kd__lte=60)
        if self.value() == 'hard':
            return queryset.filter(kd__gt=60)
        return queryset


@admin.register(KeywordResearch)
class KeywordResearchAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'intent', 'search_volume', 'kd_badge', 'cpc',
                    'priority_badge', 'market', 'article_status', 'created_at']
    list_filter = [HasArticleFilter, KDFilter, 'priority', 'market', 'intent']
    search_fields = ['keyword', 'seed_keyword']
    ordering = ['kd']
    readonly_fields = ['seed_keyword', 'keyword', 'intent', 'search_volume', 'kd',
                       'cpc', 'priority', 'market', 'created_at']
    actions = ['generate_articles_for_selected']

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom = [
            path('run-keyword-research/', self.admin_site.admin_view(self.run_keyword_research_view),
                 name='blog_keywordresearch_run'),
        ]
        return custom + urls

    def run_keyword_research_view(self, request):
        from django.shortcuts import redirect
        from django.core.management import call_command
        from django.urls import reverse

        if request.method == 'POST':
            seed = request.POST.get('seed_keyword', '').strip()
            market = request.POST.get('market', 'india')
            if seed:
                try:
                    call_command('keyword_research', seed, market=market, verbosity=0)
                    self.message_user(request, f"✅ Keyword research done for '{seed}' [{market}].")
                except Exception as exc:
                    self.message_user(request, f"❌ Failed: {exc}", level=messages.ERROR)
            else:
                self.message_user(request, "Seed keyword is required.", level=messages.WARNING)
        return redirect(reverse('admin:blog_keywordresearch_changelist'))

    def changelist_view(self, request, extra_context=None):
        from django.urls import reverse
        extra_context = extra_context or {}
        extra_context['keyword_research_url'] = reverse('admin:blog_keywordresearch_run')
        return super().changelist_view(request, extra_context)

    @admin.display(description='KD', ordering='kd')
    def kd_badge(self, obj):
        colour = '#22c55e' if obj.kd <= 30 else ('#f59e0b' if obj.kd <= 60 else '#ef4444')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;'
            'border-radius:4px;font-weight:bold">{} {}</span>',
            colour, obj.kd, obj.difficulty_label,
        )

    @admin.display(description='Priority')
    def priority_badge(self, obj):
        colours = {'High': '#16a34a', 'Medium': '#d97706', 'Low': '#6b7280'}
        c = colours.get(obj.priority, '#6b7280')
        return format_html('<b style="color:{}">{}</b>', c, obj.priority or '—')

    @admin.display(description='Blog Post')
    def article_status(self, obj):
        if obj.article:
            url = f'/sd/blog/article/{obj.article.pk}/change/'
            label = '✅ Published' if obj.article.is_published else '📝 Draft'
            return format_html('<a href="{}">{}</a>', url, label)
        return format_html('<span style="color:#9ca3af">— Not created</span>')

    @admin.action(description='🤖 Generate articles (uses Bulk Model from AI Config)')
    def generate_articles_for_selected(self, request, queryset):
        from django.core.management import call_command
        cfg = AIModelConfig.get()
        created = 0
        for kw in queryset.filter(article__isnull=True):
            try:
                call_command(
                    'generate_article', kw.keyword,
                    market=kw.market, publish=True,
                    model=cfg.bulk_model,
                    verbosity=0,
                )
                kw.refresh_from_db()
                created += 1
            except Exception as exc:
                self.message_user(
                    request,
                    f"Failed: {kw.keyword} — {exc}",
                    level=messages.ERROR,
                )
        bulk_label = dict(AIModelConfig._meta.get_field('bulk_model').choices).get(
            cfg.bulk_model, cfg.bulk_model
        )
        self.message_user(
            request,
            f"{created} article(s) generated using {bulk_label}.",
        )


# ── AI Generation Log ─────────────────────────────────────────────────────────

@admin.register(AIGenerationLog)
class AIGenerationLogAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'job_type', 'status_badge', 'market', 'model_used',
                    'token_summary', 'cost_display', 'article_link', 'duration_seconds', 'created_at']
    list_filter = ['job_type', 'status', 'market']
    search_fields = ['keyword', 'model_used']
    readonly_fields = ['job_type', 'keyword', 'market', 'model_used', 'status',
                       'output_preview', 'error_message', 'article', 'created_at',
                       'completed_at', 'duration_seconds', 'prompt_tokens',
                       'completion_tokens', 'cost_usd']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.db.models import Sum
        from .models import AIGenerationLog as Log
        totals = Log.objects.aggregate(
            total_cost=Sum('cost_usd'),
            total_prompt=Sum('prompt_tokens'),
            total_completion=Sum('completion_tokens'),
        )
        extra_context = extra_context or {}
        extra_context['total_cost']       = totals['total_cost'] or 0
        extra_context['total_prompt']     = totals['total_prompt'] or 0
        extra_context['total_completion'] = totals['total_completion'] or 0
        return super().changelist_view(request, extra_context)

    @admin.display(description='Status')
    def status_badge(self, obj):
        colours = {'done': '#16a34a', 'running': '#d97706', 'failed': '#dc2626', 'pending': '#6b7280'}
        c = colours.get(obj.status, '#6b7280')
        return format_html('<b style="color:{}">{}</b>', c, obj.get_status_display())

    @admin.display(description='Tokens (in/out)')
    def token_summary(self, obj):
        if obj.prompt_tokens or obj.completion_tokens:
            return f'{obj.prompt_tokens:,} / {obj.completion_tokens:,}'
        return '—'

    @admin.display(description='Cost (USD)', ordering='cost_usd')
    def cost_display(self, obj):
        if obj.cost_usd:
            colour = '#16a34a' if obj.cost_usd < Decimal('0.05') else (
                '#d97706' if obj.cost_usd < Decimal('0.20') else '#dc2626'
            )
            return format_html('<b style="color:{}">${}</b>', colour, f'{obj.cost_usd:.4f}')
        return '—'

    @admin.display(description='Article')
    def article_link(self, obj):
        if obj.article:
            url = f'/sd/blog/article/{obj.article.pk}/change/'
            return format_html('<a href="{}">{}</a>', url, obj.article.title[:35])
        return '—'
