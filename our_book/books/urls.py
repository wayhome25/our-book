from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list/$', views.list, name='list'),
    url(r'^purchase/$', views.puchase, name='purchase'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/save/$', views.register_save, name='register_save'),
    url(r'^list/rent/(?P<pk>\d+)/$', views.rent, name='rent'),
    url(r'^return/(?P<pk>\d+)/$', views.return_book, name='return_book'),
]