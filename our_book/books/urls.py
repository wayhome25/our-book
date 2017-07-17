from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^purchase/$', views.puchase, name='purchase'),
]