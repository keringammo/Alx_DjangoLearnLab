from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication routes from accounts app
    path('api/auth/', include('accounts.urls')),
]

