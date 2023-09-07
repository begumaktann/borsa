from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('product_list/', views.product_list, name='product_list'),
    path('add_to_cart/<int:dataset_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('download/<str:token>/', views.download, name='download'),
    path('download_link_check/<str:url_token>/', views.download_link_check, name='download_link_check'),

    # ... other URL patterns ...
]
