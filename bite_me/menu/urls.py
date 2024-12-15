from django.urls import path
from .views import menu_view, menu_edit_view, delete_menu_item, edit_menu_item

urlpatterns = [
    path('', menu_view, name='menu'),
    path('edit/', menu_edit_view, name='menu_edit'),
    path('item/<int:pk>/edit/', edit_menu_item, name='edit_menu_item'),
    path('item/<int:pk>/delete/', delete_menu_item, name='delete_menu_item'),
]
