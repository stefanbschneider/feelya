from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'app'

try:
    urlpatterns = [
        path('', views.index, name='index'),
        path('evaluate/', views.evaluate, name='evaluate')
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
except:
    urlpatterns = []
