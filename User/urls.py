from django.urls import path, include
from .views import *
from rest_framework import routers


# router = routers.DefaultRouter()
# router.register(r'update_profile', UpdateProfileView, basename='update_profile')
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('forgot-password/', ForgotPasswordViewSet.as_view(), name='forgot-password'),
    path('fp-verify/', ForgotPassVerify.as_view(), name='fp-verify'),
    path('fp-newpassword/', ForgotPassSetNewPass.as_view(), name='fp-newpassword'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='MyAuthor_change_password'),
    path('customer_profile/<int:id>/', UpdateRetrieveProfileView.as_view(), name='update-profile'),
    path('rate-restaurant/', RateRestaurantView.as_view(), name='rate-restaurant'),
    path('favorite-restaurant/', AddRemoveFavorite.as_view(), name='favorite-restaurant'),
    path('charge-wallet/', ChargeWalletView.as_view(), name='charge-wallet'),
    path('withdraw-wallet/', WithdrawFromWalletView.as_view(), name='withdraw-wallet'),
    # path('city-country/', CitiesView.as_view(), name='city-country'),
    # path('full-city-country/', FullCountryCityDict.as_view(), name='full-city-country'),
    # path('show-city-country/', ShowCountryCityDict.as_view(), name='show-city-country'),
    path('all-countries/', ShowAllCountry.as_view(), name='all-countries'),
    path('cities-of-country/', CitiesOfCountry.as_view(), name='cities-of-country'),
    path('<int:user_id>/lat_long/',LatLongUpdateRetreive.as_view(),name='get_lat_long'),
]