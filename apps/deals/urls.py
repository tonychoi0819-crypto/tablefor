from django.urls import path
from apps.deals.views import DealListView, DealDetailView, DealCreateView
from django.views.generic import UpdateView, DeleteView
from .models import Deal
app_name = 'deals'
urlpatterns = [
    path('', DealListView.as_view(), name='deal_list'),
    path('<int:pk>/', DealDetailView.as_view(), name='deal_detail'),
    path('new/<int:restaurant_id>/', DealCreateView.as_view(), name='deal_create'),
    path('<int:pk>/edit/', UpdateView.as_view(model=Deal, fields=['title','description','is_active'], template_name='deals/form.html'), name='deal_edit'),
    path('<int:pk>/delete/', DeleteView.as_view(model=Deal, template_name='deals/confirm_delete.html', success_url='/deals/'), name='deal_delete'),
]
