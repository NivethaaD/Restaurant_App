from django.urls import path
from .views import RestaurantListView , RestaurantDetailView , home , RegisterView  , BookmarkView , AddReviewView , EditReviewView, DeleteReviewView , MarkVisitedView ,VisitedView,Spotlightview
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('', home, name='home'),  
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurant/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('register/', RegisterView.as_view(template_name='registration/register.html'), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('bookmarks/', BookmarkView.as_view(), name='bookmarked_restaurants'),
    path('restaurant/<int:pk>/add-review/', AddReviewView.as_view(), name='add_review'),
    path('review/<int:pk>/edit/', EditReviewView.as_view(), name='edit_review'),
    path('review/<int:pk>/delete/', DeleteReviewView.as_view(), name='delete_review'),
    path('restaurant/<int:pk>/mark-visited/', MarkVisitedView.as_view(), name='mark_visited'),
    path('visited-restaurants/', VisitedView.as_view(), name='visited_restaurants'),
    path('spotlight-restaurants/', Spotlightview.as_view(), name='spotlighted_restaurants')

]

