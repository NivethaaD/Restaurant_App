from django.shortcuts import render
from django.views.generic import ListView , DetailView
from .models import Restaurant
from .filters import RestaurantFilter
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

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

        sort_by = self.request.GET.get('sort_by', 'rating') 
        order = self.request.GET.get('order', 'desc') 

        if sort_by == 'rating':
            if order == 'asc':
                queryset = queryset.order_by('rating') 
            else:
                queryset = queryset.order_by('-rating')  
        else:
           
            if order == 'asc':
                queryset = queryset.order_by(sort_by)
            else:
                queryset = queryset.order_by(f'-{sort_by}')

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


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your account has been created! You can now log in.')
        return super().form_valid(form)



