import django_filters
from .models import Restaurant 
from django.utils import timezone
from django.db.models import Q


class RestaurantFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(
        field_name='location',
        lookup_expr='icontains',
        label='City'
    )
    
    food_type = django_filters.ChoiceFilter(
        field_name='type_of_food',
        choices=Restaurant._meta.get_field('type_of_food').choices,
        label='Food Type'
    )
    
    cuisines = django_filters.ChoiceFilter(
        field_name='cuisines',
        choices=Restaurant._meta.get_field('cuisines').choices,
        label='Cuisines'
    )
    
    rating = django_filters.NumberFilter(
        field_name='rating',
        lookup_expr='gte',
        label='Minimum Rating'
    )
    
    cost_for_two = django_filters.NumberFilter(
        field_name='cost_for_two',
        lookup_expr='lte',
        label='Max Cost for Two'
    )
    
    open_hotel = django_filters.BooleanFilter(
        method='filter_open_hotel',
    )

    search = django_filters.CharFilter(
        method='filter_search',
        label='Search',
        widget=django_filters.widgets.LinkWidget(attrs={'placeholder': 'Search by name, city, or food type'})
    )

    ordering = django_filters.OrderingFilter(
        fields=(
            ('avg_rating', 'avg_rating'),
            ('cost_for_two', 'cost_for_two'),
        ),
        field_labels={
            'avg_rating': 'Rating',
            'cost_for_two': 'Cost for Two',
        },
        label='Sort By'
    )
    
    class Meta:
        model = Restaurant
        fields = ['city', 'food_type', 'cuisines', 'rating', 'cost_for_two']

 
    def filter_open_hotel(self, queryset, name, value):
       
        """
        Custom filter to check if the restaurant is open based on current time.
        """
        current_time = timezone.localtime(timezone.now()).time()
      
        if value: 
            filtered_queryset = queryset.filter(opening_time__lte=current_time, closing_time__gte=current_time)
            return filtered_queryset
        return queryset

    def filter_search(self, queryset, name, value):
        """
        Custom filter for search functionality. Search by name, city, or food type.
        """
        if value:
            queryset = queryset.filter(
                Q(title__icontains=value) |
                Q(location__icontains=value) |
                Q(type_of_food__icontains=value)
            )
        return queryset
    
        