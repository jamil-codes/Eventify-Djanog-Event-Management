from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path('auth/login/', views.login_view, name='login'),
    path('auth/register/', views.register_view, name='register'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/edit', views.edit_profile, name='edit_profile'),
    path('<str:username>/follow-toggle/',
         views.follow_toggle, name='follow_toggle'),
]
