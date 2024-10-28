from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_index, name='product_index'),
    path('article/<int:article_id>/', views.article_show, name='article_show'),

]