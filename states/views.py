from django.views.generic import ListView, DetailView
from .models import State


class StateListView(ListView):
    model = State
    template_name = 'states/states_index.jinja'
    context_object_name = 'states'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['meta_title'] = 'State Tax Guide India — All 28 States & UTs'
        ctx['meta_description'] = ('Professional tax slabs and income tax info '
                                   'for all Indian states FY 2025-26.')
        return ctx


class StateDetailView(DetailView):
    model = State
    template_name = 'states/state_detail.jinja'
    context_object_name = 'state'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['meta_title'] = self.object.meta_title
        ctx['meta_description'] = self.object.meta_description
        return ctx
