from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path(
        'register/', 
        views.register, 
        name='register'),

    path(
        'login/', 
        auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login',
    ),

    path('logout/', 
        auth_views.LogoutView.as_view(),
        name='logout',
    ),

    path(
        'search/', 
        views.search, 
        name='search',
    ),

    path(
        'profile/<int:user_id>/',
        views.profile,
        name='profile',
    ),

    path(
    'profile/edit/',
    views.edit_profile,
    name='edit_profile'
    ),

    path(
    'api/users/',
    views.UserListAPIView.as_view(),
    name='api_user_list'
    ),

    path(
        'api/users/<int:pk>/',
        views.UserDetailAPIView.as_view(),
        name='api_user_detail'
    ),
]