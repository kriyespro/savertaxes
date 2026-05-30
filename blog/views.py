from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Article, Category
import markdown as md


@method_decorator(cache_page(60 * 10), name='dispatch')
class ArticleListView(ListView):
    template_name = 'blog/blog_index.jinja'
    context_object_name = 'articles'
    paginate_by = 12

    def get_queryset(self):
        market = getattr(self.request, 'market', 'india')
        qs = Article.objects.published().filter(market=market).select_related('author', 'category')
        category_slug = self.kwargs.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        market = getattr(self.request, 'market', 'india')
        ctx['categories'] = Category.objects.filter(
            article__market=market, article__is_published=True
        ).distinct()
        ctx['active_category'] = self.kwargs.get('category', '')
        if market == 'us':
            ctx['meta_title'] = 'US Tax Blog 2025 — Guides for Freelancers, W-2, Investors'
            ctx['meta_description'] = ('Free US tax guides for 2025: self-employment tax, '
                                       'federal brackets, capital gains, quarterly payments and more.')
        else:
            ctx['meta_title'] = 'Indian Income Tax Blog — Tips, Guides, FY 2025-26'
            ctx['meta_description'] = ('Expert guides on income tax saving, GST, '
                                       'ITR filing, and investments for FY 2025-26.')
        return ctx


@method_decorator(cache_page(60 * 10), name='dispatch')
class ArticleDetailView(DetailView):
    template_name = 'blog/article.jinja'
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.published().select_related(
            'author', 'reviewer', 'category')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['body_html'] = md.markdown(
            self.object.body,
            extensions=['extra', 'toc', 'tables', 'nl2br']
        )
        ctx['related_articles'] = Article.objects.published().filter(
            category=self.object.category
        ).exclude(pk=self.object.pk)[:3]
        ctx['meta_title'] = self.object.meta_title
        ctx['meta_description'] = self.object.meta_description
        ctx['canonical_url'] = self.request.build_absolute_uri()
        return ctx


class ArticleHelpfulView(View):
    def post(self, request, slug):
        try:
            article = Article.objects.published().get(slug=slug)
            vote = request.POST.get('vote')
            if vote == 'yes':
                Article.objects.filter(pk=article.pk).update(
                    helpful_yes=article.helpful_yes + 1)
            elif vote == 'no':
                Article.objects.filter(pk=article.pk).update(
                    helpful_no=article.helpful_no + 1)
        except Article.DoesNotExist:
            pass
        return HttpResponse(
            '<p class="text-green-600 font-medium text-sm">Thanks for your feedback!</p>')
