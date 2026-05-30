from django.db import models
from django.utils import timezone


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
