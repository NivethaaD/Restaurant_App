from django.test import TestCase
from django.contrib.auth.models import User
from restaurant.models import Restaurant, Image, Dish, UserReview, UserBookmark, UserVisited, SpotlightRestaurant
from django.utils import timezone

# Tests For Models

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


# Test For List View

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Restaurant

class RestaurantListTestCase(TestCase):

        def setUp(self):
        # Create a user to assign as the owner
            self.user = User.objects.create_user(username='testuser', password='testpassword')

            # Create restaurants for testing
            self.restaurant_open = Restaurant.objects.create(
                title="Open Restaurant",
                location="New York",
                opening_time="10:00:00",  # Set a time that is in the future for testing
                closing_time="22:00:00",  # Set a time that is in the future for testing
                type_of_food="Italian",
                cuisines="Pizza",
                rating=4.5,
                cost_for_two=30,
                owner=self.user  
            )
            self.restaurant_closed = Restaurant.objects.create(
                title="Closed Restaurant",
                location="New York",
                opening_time="10:00:00",  
                closing_time="15:00:00", 
                type_of_food="Indian",
                cuisines="Curry",
                rating=4.0,
                cost_for_two=25,
                owner=self.user  
            )
            self.restaurant_location = Restaurant.objects.create(
                title="Location-based Restaurant",
                location="San Francisco",
                opening_time="08:00:00",  
                closing_time="20:00:00",  
                type_of_food="Mexican",
                cuisines="Tacos",
                rating=4.2,
                cost_for_two=40,
                owner=self.user  
            )

        def test_restaurant_list_url(self):
            """
            Test that the restaurant list view URL works and returns a successful response.
            """
            response = self.client.get(reverse('restaurant-list'))
            self.assertEqual(response.status_code, 200)

        def test_filter_open_restaurants(self):
            """
            Test filtering open restaurants based on current time.
            """
            current_time = timezone.now().replace(hour=14, minute=0, second=0, microsecond=0)
            timezone.now = lambda: current_time  

            response = self.client.get(reverse('restaurant-list') + '?open_hotel=true')
            self.assertContains(response, self.restaurant_open.title)
            self.assertNotContains(response, self.restaurant_closed.title)

        def test_filter_location(self):
            """
            Test filtering restaurants by location.
            """
            response = self.client.get(reverse('restaurant-list') + '?location=San Francisco')
            self.assertContains(response, self.restaurant_location.title)  

        def test_filter_rating(self):
            """
            Test filtering restaurants by rating.
            """
     
            response = self.client.get(reverse('restaurant-list') + '?rating=4.5')

            self.assertContains(response, self.restaurant_open.title)
            self.assertNotContains(response, self.restaurant_location.title)
            self.assertNotContains(response, self.restaurant_closed.title)

        def test_filter_cost_for_two(self):
            """
            Test filtering restaurants by cost for two.
            """
            response = self.client.get(reverse('restaurant-list') + '?cost_for_two=30')
            self.assertContains(response, self.restaurant_open.title)

        def test_filter_type_of_food(self):
            """
            Test filtering restaurants by type of food.
            """
            response = self.client.get(reverse('restaurant-list') + '?type_of_food=Italian')
            self.assertContains(response, self.restaurant_open.title)

# Test for the Detail view

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Restaurant, Image, Dish, User
from django.contrib.auth import get_user_model

class RestaurantDetailViewTestCase(TestCase):

    def setUp(self):
        # Create a user to assign as the owner
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

        # Create a restaurant for testing
        self.restaurant = Restaurant.objects.create(
            title="Test Restaurant",
            location="New York",
            opening_time="10:00:00",
            closing_time="22:00:00",
            type_of_food="Italian",
            cuisines="Pizza",
            rating=4.5,
            cost_for_two=30,
            owner=self.user  
        )

        # Add images to the restaurant
        self.image1 = Image.objects.create(restaurant=self.restaurant, image='image1.jpg', description='Image 1')
        self.image2 = Image.objects.create(restaurant=self.restaurant, image='image2.jpg', description='Image 2')

        # Add a menu item (dish)
        self.dish = Dish.objects.create(
            name="Spaghetti",
            price=12.99,
            restaurant=self.restaurant,
            type_of_food="veg"
        )
        self.url = reverse('restaurant_detail', args=[self.restaurant.pk])

    def test_restaurant_detail_view_status_code(self):
        """
        Test that the detail view loads successfully.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_restaurant_detail_view_template_used(self):
        """
        Test that the correct template is used for the detail view.
        """
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'restaurant/detail.html')

    def test_restaurant_title_and_details(self):
        """
        Test that the restaurant's title, description, and other details are displayed.
        """
        response = self.client.get(self.url)
        self.assertContains(response, self.restaurant.title)
        self.assertContains(response, self.restaurant.description)
        self.assertContains(response, str(self.restaurant.rating))
        self.assertContains(response, str(self.restaurant.cost_for_two))
        self.assertContains(response, self.restaurant.type_of_food)
        self.assertContains(response, self.restaurant.cuisines)

    def test_restaurant_images_display(self):
        """
        Test that images related to the restaurant are displayed.
        """
        response = self.client.get(self.url)
        self.assertContains(response, self.image1.image.url)
        self.assertContains(response, self.image2.image.url)

    def test_restaurant_menu_display(self):
        """
        Test that dishes related to the restaurant are displayed.
        """
        response = self.client.get(self.url)
        self.assertContains(response, self.dish.name)
        self.assertContains(response, str(self.dish.price))

    def test_invalid_restaurant_id(self):
        """
        Test that an invalid restaurant ID results in a 404 error.
        """
        response = self.client.get(reverse('restaurant_detail', args=[99999]))  # Non-existent restaurant ID
        self.assertEqual(response.status_code, 404)

    def test_restaurant_open_status(self):
        """
        Test that the open status of the restaurant is displayed correctly.
        """
        current_time = timezone.now().replace(hour=12, minute=0, second=0, microsecond=0)
        timezone.now = lambda: current_time  
        response = self.client.get(self.url)
        self.assertContains(response, "Open Now")

    def test_restaurant_closed_status(self):
        """
        Test that the closed status of the restaurant is displayed correctly.
        """
        current_time = timezone.now().replace(hour=23, minute=0, second=0, microsecond=0)
        timezone.now = lambda: current_time  
        response = self.client.get(self.url)
        self.assertContains(response, "Closed Now")

         
