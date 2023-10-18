from django_filters.rest_framework import FilterSet
from .models import *

class RestaurantFilter(FilterSet):
  class Meta:
    model = Restaurant
    fields = {
        'rate': ['gte', 'lte'],
        'discount': ['gte', 'lte'],
        'type': ['exact'],
    }

class FoodFilter(FilterSet):
  class Meta:
    model = Food
    fields = {
        'price': ['gte', 'lte'],
    }