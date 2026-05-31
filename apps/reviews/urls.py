from django.urls import path
from apps.reviews.views import WriteReviewView, EditReviewView, DeleteReviewView, HelpfulReviewView
app_name = 'reviews'
urlpatterns = [
    path('write/<int:restaurant_id>/', WriteReviewView.as_view(), name='write_review'),
    path('<int:pk>/edit/', EditReviewView.as_view(), name='edit_review'),
    path('<int:pk>/delete/', DeleteReviewView.as_view(), name='delete_review'),
    path('helpful/<int:pk>/', HelpfulReviewView.as_view(), name='helpful_review'),
]
