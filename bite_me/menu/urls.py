# menu/urls.py

from django.urls import path
from .views import menu_edit_view

urlpatterns = [
    path('edit/', menu_edit_view, name='menu_edit'),
]
