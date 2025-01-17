from django.shortcuts import render
from django.views.generic import ListView , DetailView , View
from .models import Restaurant, UserBookmark , UserVisited ,SpotlightRestaurant
from .filters import RestaurantFilter
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Restaurant, UserReview
from .forms import UserReviewForm, UserReviewEditForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, DecimalField
from django.db.models.functions import Coalesce


def home(request):
    return render(request,'restaurant/home.html')

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant/list.html'
    context_object_name = 'restaurants'
    paginate_by = 3

    def get_queryset(self):
      
        queryset = Restaurant.objects.annotate(
            avg_rating=Coalesce(Avg('reviews__rating'), 0 , output_field=DecimalField())  # Annotate avg_rating
        )
        restaurant_filter = RestaurantFilter(self.request.GET, queryset=queryset)
        queryset = restaurant_filter.qs 
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['food_type_choices'] = Restaurant._meta.get_field('type_of_food').choices
        context['cuisines_choices'] = Restaurant._meta.get_field('cuisines').choices
        context['rating_range']= range(5)
        return context
    
class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "restaurant/detail.html"
    context_object_name = "restaurant"
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        context['stars']= list(range(5))
        restaurant = self.get_object()
        
        # Check if the user is authenticated
        user_review = None
        if self.request.user.is_authenticated:
            user_review = UserReview.objects.filter(restaurant=restaurant, user=self.request.user).first()

        # Get all reviews for the restaurant
        reviews = UserReview.objects.filter(restaurant=restaurant)

        if reviews.exists():
            avg_rating = sum([review.rating for review in reviews]) / reviews.count()
        else:
            avg_rating = 0
        
        context['reviews'] = reviews
        context['user_review'] = user_review  # User's review if any
        context['rating_range'] = range(5)
        context['review_form'] = UserReviewForm()  # Form for adding a new review
        context['review_edit_form'] = UserReviewEditForm()  # Form for editing review
        context['avg_rating'] = avg_rating
        if self.request.user.is_authenticated:
            # Check if the user has bookmarked the restaurant
            context['is_bookmarked'] = UserBookmark.objects.filter(user=self.request.user, restaurant=restaurant).exists()
        else:
            # Set default value for unauthenticated users
            context['is_bookmarked'] = False

        if self.request.user.is_authenticated:
            context['is_visited'] = UserVisited.objects.filter(user=self.request.user, restaurant=restaurant).exists()
        else:
            context['is_visited'] = False

        isspotlight = SpotlightRestaurant.objects.filter(restaurant=restaurant , spotlighted=True)
        if isspotlight:
            context['is_spotlight']=True
        else:
            context['is_spotlight'] = False
            
        return context

class ToggleBookmarkView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        bookmark, created = UserBookmark.objects.get_or_create(user=request.user, restaurant=restaurant)

        if not created:
            # If the bookmark already exists, remove it
            bookmark.delete()
            message = "Bookmark removed"
        else:
            # If the bookmark did not exist, create it
            message = "Bookmark added"

        return redirect('restaurant_detail', pk=restaurant.pk)
    
    def get(self, request, pk, *args, **kwargs):
        return redirect('restaurant_detail', pk=pk)
    
class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        review_form = UserReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.restaurant = restaurant
            review.save()
        return redirect('restaurant_detail', pk=restaurant.pk)

class EditReviewView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        review = get_object_or_404(UserReview, pk=pk)
        if review.user != request.user:
            return redirect('restaurant_detail', pk=review.restaurant.pk)
        edit_form = UserReviewEditForm(request.POST, instance=review)
        if edit_form.is_valid():
            edit_form.save()
        return redirect('restaurant_detail', pk=review.restaurant.pk)

class DeleteReviewView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        review = get_object_or_404(UserReview, pk=pk)
        if review.user == request.user:
            review.delete()
        return redirect('restaurant_detail', pk=review.restaurant.pk)
        
class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()

        messages.success(self.request, 'Your account has been created! You can now log in.')
        return super().form_valid(form)
    
class BookmarkView(LoginRequiredMixin, ListView):
    model = Restaurant
    template_name = 'restaurant/bookmarked_restaurants.html'
    context_object_name = 'bookmarked_restaurants'

    def get_queryset(self):
        # Get the restaurants bookmarked by the logged-in user
        user = self.request.user
        # Query UserBookmark for all bookmarks by this user
        bookmarked_restaurants_ids = UserBookmark.objects.filter(user=user).values_list('restaurant_id', flat=True)
        # Retrieve restaurants using the IDs
        return Restaurant.objects.filter(id__in=bookmarked_restaurants_ids)
    

class MarkVisitedView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        restaurant = get_object_or_404(Restaurant, pk=kwargs['pk'])
        visited, created = UserVisited.objects.get_or_create(user=request.user, restaurant=restaurant)

        if not created:
            visited.delete()
            message = "Visit record removed"
        else:
            message = "Restaurant marked as visited"
        return redirect('restaurant_detail', pk=restaurant.pk)

class VisitedView(LoginRequiredMixin, ListView):
    model = Restaurant
    template_name = 'restaurant/visited_restaurants.html'
    context_object_name = 'visited_restaurants'

    def get_queryset(self):
      
        user = self.request.user
        visited_restaurants_ids = UserVisited.objects.filter(user=user).values_list('restaurant_id', flat=True)
        return Restaurant.objects.filter(id__in=visited_restaurants_ids)
    
class Spotlightview(ListView):
    model = SpotlightRestaurant
    template_name = "restaurant/spotlight_restaurants.html"
    context_object_name = 'spotlight_restaurants'



    