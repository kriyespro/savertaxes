from django.db import models


CATEGORY_CHOICES = [
    ('regime', 'Regime Comparison'),
    ('income', 'Income Tax'),
    ('deductions', 'Deductions & Savings'),
    ('freelancer', 'Freelancer & Business'),
    ('gst', 'GST'),
    ('investment', 'Investments & Capital Gains'),
    ('retirement', 'Retirement & Savings'),
    ('utility', 'Utility Tools'),
    # US categories
    ('us_income', 'US Income Tax'),
    ('us_deductions', 'US Deductions'),
    ('us_self_employment', 'US Self-Employment'),
    ('us_investment', 'US Investments'),
    ('us_retirement', 'US Retirement'),
]

MARKET_CHOICES = [
    ('india', 'India'),
    ('us', 'United States'),
    ('global', 'Global'),
]


class Tool(models.Model):
    slug = models.SlugField(unique=True, max_length=100)
    name = models.CharField(max_length=200)
    short_desc = models.CharField(max_length=300)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    market = models.CharField(max_length=10, choices=MARKET_CHOICES, default='india')
    icon = models.CharField(max_length=50, default='calculator')
    is_featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    rating_up = models.IntegerField(default=0)
    rating_down = models.IntegerField(default=0)
    meta_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=165)
    fy_applicable = models.CharField(max_length=20, default='2025-26')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('tools:detail', args=[self.slug])

    @property
    def rating_total(self):
        return self.rating_up + self.rating_down

    @property
    def rating_pct(self):
        if self.rating_total == 0:
            return 0
        return round(self.rating_up / self.rating_total * 100)
