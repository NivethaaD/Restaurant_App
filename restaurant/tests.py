from django.test import TestCase
from django.contrib.auth.models import User
from restaurant.models import Restaurant, Image, Dish, UserReview, UserBookmark, UserVisited, SpotlightRestaurant
from django.utils import timezone


class BaseTest(TestCase):

    def setUp(self):
     
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.restaurant = Restaurant.objects.create(
            title="Test Restaurant",
            description="Sample Description",
            rating=4.5,
            cost_for_two=500.00,
            location="Sample Location",
            address="123 Sample Street",    
            type_of_food="veg",  
            cuisines="indian",  
            owner=self.user,
        )


class RestaurantModelTest(BaseTest):
 
    current_time = timezone.localtime().time()
    def test_restaurant_creation(self):
        self.assertEqual(self.restaurant.title, "Test Restaurant")
        self.assertTrue(self.restaurant.opening_time <= self.current_time <= self.restaurant.closing_time)

class ImageModelTest(BaseTest):

    def test_image_creation(self):
        image = Image.objects.create(
            restaurant=self.restaurant,
            image="path/to/image.jpg",
            description="Sample Image"
        )
        self.assertEqual(image.restaurant, self.restaurant)

class DishModelTest(BaseTest):
  
    def test_dish_creation(self):
        dish = Dish.objects.create(
            restaurant=self.restaurant,
            name="Sample Dish",
            price=150.00,
            type_of_food="veg"
        )
        self.assertEqual(dish.restaurant, self.restaurant)

class UserReviewModelTest(BaseTest):

    def test_user_review_creation(self):
        review = UserReview.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            review_text="Great food!",
            rating=4.5
        )
        self.assertEqual(review.restaurant, self.restaurant)

class UserBookmarkModelTest(BaseTest):
  
    def test_user_bookmark_creation(self):
        bookmark = UserBookmark.objects.create(
            restaurant=self.restaurant,
            user=self.user
        )
        self.assertEqual(bookmark.restaurant, self.restaurant)

class UserVisitedModelTest(BaseTest):

    def test_user_visited_creation(self):
        visited = UserVisited.objects.create(
            restaurant=self.restaurant,
            user=self.user
        )
        self.assertEqual(visited.restaurant, self.restaurant)

class SpotlightRestaurantModelTest(BaseTest):
  
    def test_spotlight_restaurant_creation(self):
        spotlight = SpotlightRestaurant.objects.create(
            restaurant=self.restaurant,
            spotlighted=True
        )
        self.assertTrue(spotlight.spotlighted)
