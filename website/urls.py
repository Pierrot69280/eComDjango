from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_index, name='product_index'),
    path('product/<int:product_id>/', views.product_show, name='product_show'),

]