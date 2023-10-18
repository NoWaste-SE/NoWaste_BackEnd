from django.urls import path, include
from .views import *
# from rest_framework import routers
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('restaurant-search', RestaurantSearchViewSet, basename='restaurant-search')
router.register('restaurant_profile',RestaurantProfileViewSet,basename = 'rest-profile')
router.register('filter-food', FilterFoodViewSet, basename='filter-food')

restaurant_router = routers.NestedSimpleRouter(router, 'restaurant_profile', lookup='id')
restaurant_router.register('food', FoodViewSet, basename='restaurant-food')

order_router = routers.NestedSimpleRouter(router, 'restaurant_profile', lookup='id')


router.register('restaurant_view', RestaurantCustomerView, basename='restaurant')

restaurant_router = routers.NestedSimpleRouter(router, 'restaurant_view', lookup='restaurant')
restaurant_router.register('food', FoodViewSet, basename='restaurant-food')


urlpatterns = [
    path(r'', include(router.urls)),
    # path(r'', include(order_router.urls)),
    path('<int:manager_id>/orderview/',RestaurantOrderViewAPI.as_view(),name = 'restaurant-orders-view'),
    path('restaurant_view/<int:restaurant_id>/<int:userId>/order/',OrderAPIView.as_view(), name = 'order-detail'),
    path('restaurant_view/<int:restaurant_id>/<int:userId>/order/<uuid:order_id>/',UpdateOrderStatusAPI.as_view(), name = 'update-order-status'),
    path('restaurant_view/<int:restaurant_id>/<int:userId>/order/add_to_order/<int:food_id>/',add_to_Order, name = 'add-to-order'),
    path('restaurant_view/<int:restaurant_id>/<int:userId>/order/remove_from_order/<int:food_id>/',remove_from_Order, name = 'remove-from-order'),
    path('customer/<int:user_id>/orderview/', CustomerOrderViewAPI.as_view(),name = 'cutomer-orders-view'),
    path('managers/<int:pk>/', RestaurantManagerDetailView.as_view(), name='manager-detail'),
    path('managers/<int:manager_id>/restaurants/', RestaurantManagerRestaurantListView.as_view(), name='restaurant-list'),
    path('managers/<int:manager_id>/restaurants/<int:pk>/', RestaurantManagerRestaurantDetailView.as_view(), name='restaurant-detail'),
    path('managers/<int:manager_id>/restaurants/<int:restaurant_id>/food/', ManagerFoodListCreateAPIView.as_view(), name='food-list'),
    path('managers/<int:manager_id>/restaurants/<int:restaurant_id>/food/<int:pk>/',  ManagerFoodViewSet.as_view(), name='food-detail'),
    path('comment/user_id/<int:user_id>/restaurant_id/<int:restaurant_id>/', CommentAPI.as_view(), name='comment'),
    path('restaurant_id/<int:restaurant_id>/comments/', RestaurantCommentListAPIView.as_view(), name='restaurant-comments'),
    # path('nearest_restaurant/<str:origin>',search_nearest_restaurant,name='search_nearest_restaurant'),
    path('nearest_restaurant',SearchNearestRestaurant.search_nearest_restaurant,name='search_nearest_restaurant'),
    path('getaddr',get_addr,name='get_addr'),
    path('<int:restaurant_id>/lat_long',LatLongUpdateRetreive.as_view(),name='get_update_lat_long'),
]



