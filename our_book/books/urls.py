from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^purchase/$', views.puchase, name='purchase'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/save/$', views.register_save, name='register_save'),
]