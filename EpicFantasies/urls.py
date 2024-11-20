
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from epicfantasiesapp.views import error404
from django.conf.urls import handler404

handler404 = error404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('epicfantasiesapp.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)