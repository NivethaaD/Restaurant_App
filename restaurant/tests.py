from django.test import TestCase
from django.contrib.auth.models import User
from restaurant.models import Restaurant, Image, Dish, UserReview, UserBookmark, UserVisited, SpotlightRestaurant

class RestaurantModelTest(TestCase):
    def setUp(self):
        """Create test data."""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.restaurant = Restaurant.objects.create(
            title="Test Restaurant",
            description="Sample Description",
            rating=4.5,
            cost_for_two=500.00,
            location="Sample Location",
            address="123 Sample Street", 
            timings="9 AM to 9 PM",  
            type_of_food="veg",  
            cuisines="indian",  
            owner=self.user
        )

    def test_restaurant_creation(self):
        """Test restaurant creation."""
        self.assertEqual(self.restaurant.title, "Test Restaurant")

class ImageModelTest(TestCase):
    def setUp(self):
        """Create test data."""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.restaurant = Restaurant.objects.create(
            title="Test Restaurant",
            description="Sample Description",
            rating=4.5,
            cost_for_two=500.00,
            location="Sample Location",
            address="123 Sample Street",  
            timings="9 AM to 9 PM",  
            type_of_food="veg",  
            cuisines="indian", 
            owner=self.user
        )

    def test_image_creation(self):
        """Test image creation and association with restaurant."""
        image = Image.objects.create(
            restaurant=self.restaurant,
            image="path/to/image.jpg",
            description="Sample Image"
        )
        self.assertEqual(image.restaurant, self.restaurant)

class DishModelTest(TestCase):
    def setUp(self):
        """Create test data."""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.restaurant = Restaurant.objects.create(
            title="Test Restaurant",
            description="Sample Description",
            rating=4.5,
            cost_for_two=500.00,
            location="Sample Location",
            address="123 Sample Street",  
            timings="9 AM to 9 PM",  
            type_of_food="veg",  
            cuisines="indian", 
            owner=self.user
        )

    def test_dish_creation(self):
        """Test dish creation and association with restaurant."""
        dish = Dish.objects.create(
            restaurant=self.restaurant,
            name="Sample Dish",
            price=150.00,
            type_of_food="veg"
        )
        self.assertEqual(dish.restaurant, self.restaurant)

class UserReviewModelTest(TestCase):
    def setUp(self):
        """Create test data."""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.restaurant = Restaurant.objects.create(
            title="Test Restaurant",
            description="Sample Description",
            rating=4.5,
            cost_for_two=500.00,
            location="Sample Location",
            address="123 Sample Street",  
            timings="9 AM to 9 PM",  
            type_of_food="veg",  
            cuisines="indian", 
            owner=self.user
        )

    def test_user_review_creation(self):
        """Test user review creation."""
        review = UserReview.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            review_text="Great food!",
            rating=4.5
        )
        self.assertEqual(review.restaurant, self.restaurant)

class UserBookmarkModelTest(TestCase):
    def setUp(self):
        """Create test data."""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.restaurant = Restaurant.objects.create(
            title="Test Restaurant",
            description="Sample Description",
            rating=4.5,
            cost_for_two=500.00,
            location="Sample Location",
            address="123 Sample Street", 
            timings="9 AM to 9 PM",  
            type_of_food="veg",  
            cuisines="indian",  
            owner=self.user
        )

    def test_user_bookmark_creation(self):
        """Test user bookmarking a restaurant."""
        bookmark = UserBookmark.objects.create(
            restaurant=self.restaurant,
            user=self.user
        )
        self.assertEqual(bookmark.restaurant, self.restaurant)

class UserVisitedModelTest(TestCase):
    def setUp(self):
        """Create test data."""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.restaurant = Restaurant.objects.create(
            title="Test Restaurant",
            description="Sample Description",
            rating=4.5,
            cost_for_two=500.00,
            location="Sample Location",
            address="123 Sample Street",  
            timings="9 AM to 9 PM",
            type_of_food="veg",  
            cuisines="indian",
            owner=self.user
        )

    def test_user_visited_creation(self):
        """Test user visiting a restaurant."""
        visited = UserVisited.objects.create(
            restaurant=self.restaurant,
            user=self.user
        )
        self.assertEqual(visited.restaurant, self.restaurant)

class SpotlightRestaurantModelTest(TestCase):
    def setUp(self):
        """Create test data."""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.restaurant = Restaurant.objects.create(
            title="Test Restaurant",
            description="Sample Description",
            rating=4.5,
            cost_for_two=500.00,
            location="Sample Location",
            address="123 Sample Street",  
            timings="9 AM to 9 PM", 
            type_of_food="veg", 
            cuisines="indian",  
            owner=self.user
        )

    def test_spotlight_restaurant_creation(self):
        """Test spotlighting a restaurant."""
        spotlight = SpotlightRestaurant.objects.create(
            restaurant=self.restaurant,
            spotlighted=True
        )
        self.assertTrue(spotlight.spotlighted)
