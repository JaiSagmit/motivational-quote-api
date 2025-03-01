from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('quotes.urls')),  # Add this line to include your quotes API URLs
]
