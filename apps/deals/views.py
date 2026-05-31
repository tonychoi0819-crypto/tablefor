from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Deal

class DealListView(ListView):
    model = Deal
    template_name = 'deals/list.html'
    context_object_name = 'deals'
    def get_queryset(self):
        from django.utils import timezone
        return Deal.objects.filter(is_active=True, end_date__gte=timezone.now())

class DealDetailView(DetailView):
    model = Deal
    template_name = 'deals/detail.html'

class DealCreateView(LoginRequiredMixin, CreateView):
    model = Deal
    fields = ['title', 'description', 'deal_type', 'discount_percent', 'discount_amount', 'min_spending', 'terms', 'start_date', 'end_date']
    template_name = 'deals/form.html'
    def form_valid(self, form):
        form.instance.restaurant_id = self.kwargs.get('restaurant_id')
        return super().form_valid(form)
