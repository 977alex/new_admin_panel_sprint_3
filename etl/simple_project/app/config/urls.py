from django.contrib import admin
from django.urls import path, include

from . import settings

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('movies.api.urls')),
        path('debug/', include(debug_toolbar.urls)),
    ]
else:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('movies.api.urls')),
    ]
