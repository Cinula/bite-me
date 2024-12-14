from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),  # Routes to booking app
    path('menu/', include('menu.urls')),  # Routes to menu app
]
