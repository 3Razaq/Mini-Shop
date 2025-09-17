from django.urls import path
from . import views


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/confirm/', views.order_confirm, name='order_confirm'),
]


