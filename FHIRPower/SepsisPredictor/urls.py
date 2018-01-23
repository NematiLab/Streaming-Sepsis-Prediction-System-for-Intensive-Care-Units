from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_data/(?P<increment>[0-9]+)/$', views.get_data, name='get_data'),
    url(r'^get_detail_data/(?P<patient_id>[0-9]+)/(?P<increment>[0-9]+)/$', views.get_detail_data, name='get_detail_data'),
    url(r'^(?P<patient_id>[0-9]+)/$', views.detail, name='detail'),
]