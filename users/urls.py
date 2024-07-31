from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', signup, name = 'signup'),
    path('signin/', signin, name = 'signin'),
    path('profile/', profile, name = 'profile'),
    path('logout/', logout_view, name = 'logout'),
    # path("change-password/", auth_views.PasswordChangeView.as_view()),
    # path('login/', auth_views.LoginView, name='login')

] 
