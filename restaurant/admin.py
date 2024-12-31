from django.contrib import admin
from .models import Restaurant, Image, Dish, UserReview, UserBookmark, UserVisited, SpotlightRestaurant

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'cost_for_two', 'location', 'owner', 'created_at')
    search_fields = ('title', 'location', 'owner__username')
    list_filter = ('type_of_food', 'cuisines', 'owner')

class ImageAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'description', 'created_at')
    search_fields = ('restaurant__title', 'description')

class DishAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'name', 'price', 'type_of_food')
    search_fields = ('restaurant__title', 'name')
    list_filter = ('type_of_food',)

class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'rating', 'created_at')
    search_fields = ('restaurant__title', 'user__username')

class UserBookmarkAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'created_at')
    search_fields = ('restaurant__title', 'user__username')

class UserVisitedAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'visited_at')
    search_fields = ('restaurant__title', 'user__username')

class SpotlightRestaurantAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'spotlighted')
    search_fields = ('restaurant__title',)

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(UserReview, UserReviewAdmin)
admin.site.register(UserBookmark, UserBookmarkAdmin)
admin.site.register(UserVisited, UserVisitedAdmin)
admin.site.register(SpotlightRestaurant, SpotlightRestaurantAdmin)
