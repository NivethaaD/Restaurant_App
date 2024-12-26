from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    cost_for_two = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    address = models.TextField()
    timings = models.CharField(max_length=255)
    type_of_food = models.CharField( 
        max_length=10,
        choices=[('veg', 'Veg'), ('non-veg', 'Non-Veg'), ('vegan', 'Vegan')]
    )
    cuisines = models.CharField(
        max_length=255,
        choices=[('indian', 'Indian'), ('chinese', 'Chinese'), ('italian', 'Italian'),
                 ('mexican', 'Mexican'), ('japanese', 'Japanese'), ('continental', 'Continental')]
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_restaurants') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_images/') 
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for {self.restaurant.title}"


class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menu', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type_of_food = models.CharField( 
        max_length=10,
        choices=[('veg', 'Veg'), ('non-veg', 'Non-Veg'), ('vegan', 'Vegan')]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.restaurant.title} by {self.user.username}"


class UserBookmark(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='bookmarks', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bookmark for {self.restaurant.title} by {self.user.username}"


class UserVisited(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='visited', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visited {self.restaurant.title} by {self.user.username}"


class SpotlightRestaurant(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    spotlighted = models.BooleanField(default=False)

    def __str__(self):
        return f"{'Spotlighted' if self.spotlighted else 'Not Spotlighted'} - {self.restaurant.title}"
