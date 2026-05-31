from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q, Avg, Count
from .models import Restaurant, District, Cuisine, Tag, MenuItem, RestaurantPhoto

class HomeView(TemplateView):
    template_name = 'restaurants/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_restaurants'] = Restaurant.objects.filter(
            is_featured=True, status__in=['verified', 'claimed']
        ).select_related('district')[:8]
        context['latest_restaurants'] = Restaurant.objects.filter(
            status__in=['verified', 'claimed']
        ).select_related('district').order_by('-created_at')[:12]
        context['top_rated'] = Restaurant.objects.filter(
            status__in=['verified', 'claimed'], review_count__gte=5
        ).order_by('-avg_rating')[:8]
        context['districts'] = District.objects.all().order_by('region', 'name_en')
        context['cuisines'] = Cuisine.objects.all()[:20]
        return context

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/list.html'
    context_object_name = 'restaurants'
    paginate_by = 24
    def get_queryset(self):
        qs = Restaurant.objects.filter(
            status__in=['verified', 'claimed']
        ).select_related('district').prefetch_related('cuisines')
        district = self.request.GET.get('district')
        if district:
            qs = qs.filter(district__name_en__iexact=district)
        cuisine = self.request.GET.get('cuisine')
        if cuisine:
            qs = qs.filter(cuisines__name_en__icontains=cuisine)
        price = self.request.GET.get('price')
        if price:
            qs = qs.filter(price_range=price)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(name_en__icontains=q) | Q(name_tc__icontains=q) |
                Q(address_en__icontains=q) | Q(cuisines__name_en__icontains=q)
            ).distinct()
        sort = self.request.GET.get('sort', 'rating')
        if sort == 'rating':
            qs = qs.order_by('-avg_rating', '-review_count')
        elif sort == 'newest':
            qs = qs.order_by('-created_at')
        elif sort == 'reviews':
            qs = qs.order_by('-review_count')
        return qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['districts'] = District.objects.all().order_by('region', 'name_en')
        context['cuisines'] = Cuisine.objects.all()[:20]
        return context

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/detail.html'
    context_object_name = 'restaurant'
    slug_url_kwarg = 'slug'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.get_object()
        context['reviews'] = restaurant.reviews.filter(
            is_published=True
        ).select_related('user').order_by('-created_at')[:20]
        context['menu_items'] = restaurant.menu_items.filter(
            is_available=True
        ).order_by('category', 'name_en')
        context['photos'] = restaurant.photos.all()[:12]
        context['similar_restaurants'] = Restaurant.objects.filter(
            cuisines__in=restaurant.cuisines.all(),
            status__in=['verified', 'claimed']
        ).exclude(pk=restaurant.pk).distinct()[:4]
        return context

class CuisineListView(TemplateView):
    template_name = 'restaurants/cuisines.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cuisines'] = Cuisine.objects.all()
        return context

class DistrictListView(TemplateView):
    template_name = 'restaurants/districts.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['districts'] = District.objects.all().order_by('region', 'name_en')
        return context
