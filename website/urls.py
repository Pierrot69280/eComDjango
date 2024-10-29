from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_index, name='product_index'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/<int:product_id>/', views.product_show, name='product_show'),
    path('product/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('product/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]
