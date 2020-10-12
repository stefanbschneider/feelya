from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'app'

urlpatterns = [
    path('', views.index, name='index')
]
