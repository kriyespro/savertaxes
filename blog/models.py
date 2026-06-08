from django.db import models
from django.utils import timezone

AI_MODEL_CHOICES = [
    # ── Claude ──────────────────────────────────────────────────────────
    ('anthropic/claude-sonnet-4.6',      'Claude Sonnet 4.6  — $3.00/1M  ★ Best quality'),
    ('anthropic/claude-sonnet-4.5',      'Claude Sonnet 4.5  — $3.00/1M'),
    ('anthropic/claude-haiku-4.5',       'Claude Haiku 4.5   — $1.00/1M  ⚡ Fast'),
    ('anthropic/claude-opus-4.8',        'Claude Opus 4.8    — $5.00/1M  🏆 Top tier'),
    # ── Gemini ──────────────────────────────────────────────────────────
    ('google/gemini-2.5-pro',            'Gemini 2.5 Pro     — $1.25/1M  🔬 Deep research'),
    ('google/gemini-2.5-flash',          'Gemini 2.5 Flash   — $0.30/1M  ⚡ Balanced'),
    ('google/gemini-2.5-flash-lite',     'Gemini 2.5 Flash Lite — $0.10/1M 💰 Ultra cheap'),
    ('google/gemini-3.1-flash-lite',     'Gemini 3.1 Flash Lite — $0.25/1M'),
    ('google/gemini-3.5-flash',          'Gemini 3.5 Flash   — $1.50/1M  🆕 Latest'),
    # ── DeepSeek ────────────────────────────────────────────────────────
    ('deepseek/deepseek-chat-v3-0324',   'DeepSeek V3        — $0.20/1M  💰 Cheap bulk'),
    ('deepseek/deepseek-v3.1-terminus',  'DeepSeek V3.1      — $0.27/1M'),
    ('deepseek/deepseek-v4-flash',       'DeepSeek V4 Flash  — $0.10/1M  💰 Cheapest'),
    ('deepseek/deepseek-r1-0528',        'DeepSeek R1        — $0.50/1M  🧠 Reasoning'),
    # ── OpenAI ──────────────────────────────────────────────────────────
    ('openai/gpt-4o',                    'GPT-4o             — $2.50/1M'),
    ('openai/gpt-4o-mini',               'GPT-4o Mini        — $0.15/1M  💰 Cheap'),
]

DEFAULT_KEYWORD_MODEL   = 'google/gemini-2.5-flash'      # sweet spot for structured tables
DEFAULT_ARTICLE_MODEL   = 'anthropic/claude-sonnet-4.6'  # best instruction following + English
DEFAULT_BULK_MODEL      = 'google/gemini-2.5-flash'      # reliable English, 4x cheaper than Pro
DEFAULT_HUMANIZE_MODEL  = 'google/gemini-2.5-flash'      # cheap + good at style rewrites


JOB_STATUS = [
    ('pending', 'Pending'),
    ('running', 'Running'),
    ('done', 'Done'),
    ('failed', 'Failed'),
]

JOB_TYPE = [
    ('keyword', 'Keyword Research'),
    ('article', 'Article Generation'),
]


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    photo = models.ImageField(upload_to='authors/', blank=True)
    is_ca = models.BooleanField(default=False)
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} — {self.title}"


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(is_published=True, published_at__lte=timezone.now())


MARKET_CHOICES = [('india', 'India'), ('us', 'United States'), ('global', 'Global')]


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    market = models.CharField(max_length=10, choices=MARKET_CHOICES, default='india')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True,
                               related_name='articles')
    reviewer = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True,
                                 blank=True, related_name='reviewed_articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.CharField(max_length=500, blank=True)
    body = models.TextField()
    excerpt = models.TextField(max_length=400)
    featured_image = models.ImageField(upload_to='articles/', blank=True)
    fy_applicable = models.CharField(max_length=20, default='2025-26')
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=165)
    related_tools = models.ManyToManyField('tools.Tool', blank=True)
    reading_time = models.IntegerField(default=5)
    helpful_yes = models.IntegerField(default=0)
    helpful_no = models.IntegerField(default=0)

    objects = ArticleManager()

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:detail', args=[self.slug])

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]


INTENT_CHOICES = [
    ('Informational', 'Informational'),
    ('Transactional', 'Transactional'),
    ('Commercial', 'Commercial'),
    ('Navigational', 'Navigational'),
]

PRIORITY_CHOICES = [
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
]


class KeywordResearch(models.Model):
    seed_keyword = models.CharField(max_length=300)
    keyword = models.CharField(max_length=300, unique=True)
    intent = models.CharField(max_length=30, choices=INTENT_CHOICES, blank=True)
    search_volume = models.CharField(max_length=30, blank=True)
    kd = models.IntegerField(default=0, help_text='Keyword Difficulty 0-100')
    cpc = models.CharField(max_length=20, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, blank=True)
    market = models.CharField(max_length=10, default='india')
    article = models.ForeignKey(
        'Article', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='keywords',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['kd']
        verbose_name = 'Keyword'
        verbose_name_plural = 'Keyword Research'

    def __str__(self):
        return f"{self.keyword} (KD={self.kd})"

    @property
    def difficulty_label(self):
        if self.kd <= 30:
            return 'Easy'
        if self.kd <= 60:
            return 'Moderate'
        return 'Hard'


class AIModelConfig(models.Model):
    """Singleton. One row only — stores which model to use for each task."""
    keyword_model = models.CharField(
        max_length=100, choices=AI_MODEL_CHOICES, default=DEFAULT_KEYWORD_MODEL,
        verbose_name='Keyword Research Model',
        help_text='Used by: python manage.py keyword_research',
    )
    article_model = models.CharField(
        max_length=100, choices=AI_MODEL_CHOICES, default=DEFAULT_ARTICLE_MODEL,
        verbose_name='Article Generation Model',
        help_text='Used by: python manage.py generate_article (single article)',
    )
    bulk_model = models.CharField(
        max_length=100, choices=AI_MODEL_CHOICES, default=DEFAULT_BULK_MODEL,
        verbose_name='Bulk Generation Model',
        help_text='Used by: admin "Generate articles" bulk action',
    )
    humanize_model = models.CharField(
        max_length=100, choices=AI_MODEL_CHOICES, default=DEFAULT_HUMANIZE_MODEL,
        verbose_name='Humanization Model (Pipeline Step 4)',
        help_text='Adds practitioner observations, real-world scenario, removes marketing language',
    )
    articles_per_hour = models.IntegerField(
        default=5,
        verbose_name='Articles Per Hour (autopublish rate)',
        help_text=(
            'How many articles autopublish generates per cron run. '
            'Sets the delay between articles: 3600 ÷ this number (seconds). '
            'E.g. 5 = one article every 12 min. Max 20 recommended.'
        ),
    )
    is_paused = models.BooleanField(
        default=False,
        verbose_name='Pause Autopublish',
        help_text='When checked, the autopublish command exits immediately without generating any articles.',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'AI Model Configuration'
        verbose_name_plural = 'AI Model Configuration'

    def __str__(self):
        return 'AI Model Config'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AIGenerationLog(models.Model):
    job_type = models.CharField(max_length=20, choices=JOB_TYPE)
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='pending')
    keyword = models.CharField(max_length=300)
    market = models.CharField(max_length=10, default='india')
    model_used = models.CharField(max_length=100, blank=True)
    output_preview = models.TextField(blank=True)
    article = models.ForeignKey(Article, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='ai_logs')
    error_message = models.TextField(blank=True)
    # Token + cost tracking
    prompt_tokens = models.IntegerField(default=0)
    completion_tokens = models.IntegerField(default=0)
    cost_usd = models.DecimalField(max_digits=8, decimal_places=6, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'AI Generation Log'
        verbose_name_plural = 'AI Generation Logs'

    def __str__(self):
        return f"[{self.get_job_type_display()}] {self.keyword} — {self.status}"

    @property
    def duration_seconds(self):
        if self.completed_at and self.created_at:
            return (self.completed_at - self.created_at).seconds
        return None
