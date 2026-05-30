from django.views.generic import TemplateView


class GSTIndexView(TemplateView):
    template_name = 'gst/gst_index.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['meta_title'] = 'GST Calculator & Tools India 2025 — Free'
        ctx['meta_description'] = ('Free GST calculator, reverse GST, '
                                   'and registration checker for India.')
        return ctx
