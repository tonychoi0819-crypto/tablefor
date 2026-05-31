from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Review, ReviewHelpful
from apps.restaurants.models import Restaurant

class WriteReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'title', 'body', 'meal_type', 'visit_date', 'party_size', 'spending_per_head']
    template_name = 'reviews/write.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.restaurant = get_object_or_404(Restaurant, pk=self.kwargs['restaurant_id'])
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('restaurants:restaurant_detail', kwargs={'slug': self.object.restaurant.slug})

class EditReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['rating', 'title', 'body', 'meal_type', 'visit_date', 'party_size']
    template_name = 'reviews/write.html'
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    def get_success_url(self):
        return reverse_lazy('restaurants:restaurant_detail', kwargs={'slug': self.object.restaurant.slug})

class HelpfulReviewView(LoginRequiredMixin, View):
    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        vote, created = ReviewHelpful.objects.get_or_create(review=review, user=request.user)
        if not created:
            vote.delete()
            review.helpful_count = max(0, review.helpful_count - 1)
        else:
            review.helpful_count += 1
        review.save(update_fields=['helpful_count'])
        return redirect('restaurants:restaurant_detail', slug=review.restaurant.slug)
