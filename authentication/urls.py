from django.urls import path
from authentication import views

urlpatterns = [
    # User Authentication and Token Management
    path('login/', views.CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('verify/', views.CustomTokenVerifyView.as_view(), name='token_verify'),
    path('refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),

    # User Registration
    path("verify-email", views.GenerateEmailOTPAPIView.as_view(),name="verify-email",),
    path("verify-phone", views.GeneratePhoneOTPAPIView.as_view(),name="verify-phone",),
    path("verify-otp", views.VerifyOTPAPIView.as_view(),name="verify-otp",),
    path("register", views.UserRegistrationAPIView.as_view(),name="user-register-api",),

    # User Profile and Activity
    path('profile/', views.ProfileListAPIView.as_view(), name='profile'),
    path('profile/update-profile-picture', views.ProfilePictureUpdateAPIView.as_view(), name='profile-update-profile-picture'),
    path('profile/recent-activity', views.RecentActivityListAPIView.as_view(), name='profile-recent-activity'),
    
]

