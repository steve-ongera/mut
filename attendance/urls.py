
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('check-in/', views.check_in, name='check_in'),
    path('view-attendance/', views.view_attendance, name='view_attendance'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
  
]
