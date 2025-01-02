from django.shortcuts import render
from django.views.generic import ListView , DetailView
from .models import Restaurant
from .filters import RestaurantFilter

def home(request):
    return render(request,'restaurant/home.html')

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant/list.html'
    context_object_name = 'restaurants'
    paginate_by = 3

    def get_queryset(self):
        queryset = Restaurant.objects.all()
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
        return context





