import datetime

from django.urls import path, include, re_path, register_converter
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views


app_name = 'app'


class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value


register_converter(DateConverter, 'yyyymmdd')


urlpatterns = [
    path('', include('pwa.urls')),
    path('', views.redirect_landing_page, name='redirect'),
    path('about/', TemplateView.as_view(template_name='app/about.html'), name='about'),
    path('track/', views.index, name='index'),

    path('<yyyymmdd:init_date>/', views.index, name='index_with_date'),
    path('add/<entry_name>/', views.add_entry, name='add'),
    path('add/<entry_name>/<yyyymmdd:entry_date>/', views.add_entry, name='add_entry_with_date'),
    path('delete/<int:pk>/', views.delete_entry, name='delete'),
    path('evaluate/total/', views.evaluate, name='evaluate'),
    path('evaluate/time/', views.eval_time_series, name='eval_time_series'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
