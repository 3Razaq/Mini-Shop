from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/orders/', views.order_history, name='order_history'),
]


