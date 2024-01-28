from django.urls import path, include
from .views import *
from rest_framework import routers



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
    path('all-countries/', ShowAllCountry.as_view(), name='all-countries'),
    path('cities-of-country/', CitiesOfCountry.as_view(), name='cities-of-country'),
    path('<int:user_id>/lat_long/',LatLongUpdateRetreive.as_view(),name='get_lat_long'),
    path('excel/restaurants-info/', RestaurantInfoExportExcel.as_view(), name='csv-restaurants-info'),
    path('all_restaurants/', GetRestaurants.as_view(), name='all_restaurants'),
    path('all_customers/', GetCustomers.as_view(), name='all_customers'),
    # path('temp-manager/',TempManagerConfirmation.as_view(),name='add-delete-tmpMng'),
    path('temp-manager-confirm/',TempManagerConfirmation.as_view(),name='confirm-tmpMng'),
    path('temp-manager-reject/<int:pk>/',TempManagerRejection.as_view(),name='reject-tmpMng'),
    # path('accept/', AcceptByAdminView.as_view(), name='accept'),
    # path('reject/', RejectByAdminView.as_view(), name='reject'),
    path('admin-profile/', AdminProfile.as_view(), name='admin-profile'),
]