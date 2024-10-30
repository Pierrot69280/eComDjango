from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_index, name='product_index'),
    path('product/<int:product_id>/', views.product_show, name='product_show'),
    path('orders/', views.order_list, name='order_list'),
    path('product/<int:product_id>/add_to_order/', views.add_product_to_order, name='add_product_to_order'),
    path('order/item/<int:product_id>/delete/', views.order_item_delete, name='order_item_delete'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('comment/<int:comment_id>/edit/', views.comment_edit, name='comment_edit'),
    path('product/<int:product_id>/add_comment/', views.add_comment, name='add_comment'),
    path('payment/create-checkout-session/<int:order_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel.html'),
    path('payment/create-checkout-session/<int:order_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]
