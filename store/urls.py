from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/categories/', views.api_categories, name='api_categories'),
    path('api/products/', views.api_products, name='api_products'),
    path('api/products/<int:pk>/', views.api_product_detail, name='api_product_detail'),
    path('api/cart/', views.api_cart, name='api_cart'),
    path('api/checkout/', views.api_checkout, name='api_checkout'),
    path('api/orders/', views.api_orders, name='api_orders'),
    path('api/auth/register/', views.api_register, name='api_register'),
    path('api/auth/login/', views.api_login, name='api_login'),
    path('api/auth/logout/', views.api_logout, name='api_logout'),
    path('api/auth/me/', views.api_me, name='api_me'),
]
