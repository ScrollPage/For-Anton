from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from question.views import EmptyRouteView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('account/', include('account.urls')),
    path('question/', include('question.urls')),
    path('', EmptyRouteView.as_view(), name='empty'),

    path('auth/', include('djoser.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)