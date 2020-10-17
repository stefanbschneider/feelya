from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/<entry_name>/', views.add_entry, name='add'),
    path(r'^add/<entry_name>/(?P<entry_date>\d{4}-\d{2}-\d{2})/$', views.add_entry, name='add_with_date'),
    path('delete/<int:pk>/', views.delete_entry, name='delete'),
    path('evaluate/', views.evaluate, name='evaluate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
