from django.urls import path
from .views import menu_view, menu_edit_view

urlpatterns = [
    path('', menu_view, name='menu'),
    path('edit/', menu_edit_view, name='menu_edit'),
]
