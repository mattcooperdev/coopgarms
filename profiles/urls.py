from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name="profile"),
    path('delete_profile/', views.deleteProfile, name='delete_profile'),
    path('order_history/<order_number>', views.order_history,
         name="order_history"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:id>", views.add_to_wishlist,
         name="user_wishlist"),
]
