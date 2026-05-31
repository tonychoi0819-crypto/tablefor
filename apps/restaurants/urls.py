from django.urls import path
from apps.restaurants.views import (
    HomeView,
    RestaurantListView,
    RestaurantDetailView,
    CuisineListView,
    DistrictListView,
)

app_name = 'restaurants'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', RestaurantListView.as_view(), name='search'),
    path('cuisines/', CuisineListView.as_view(), name='cuisines'),
    path('districts/', DistrictListView.as_view(), name='districts'),
    path('<slug:slug>/', RestaurantDetailView.as_view(), name='restaurant_detail'),
]
