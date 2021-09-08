from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('password/', views.ChangePasswordView.as_view(), name='password'),

]
