from django.db import models


class State(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    abbr = models.CharField(max_length=3)
    has_professional_tax = models.BooleanField(default=False)
    prof_tax_slabs_json = models.TextField(blank=True)
    gst_state_code = models.CharField(max_length=2, blank=True)
    special_notes = models.TextField(blank=True)
    meta_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=165)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('states:detail', args=[self.slug])
