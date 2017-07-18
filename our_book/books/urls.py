from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list/$', views.list, name='list'),
    url(r'^wish/$', views.wish_books, name='wish'),
    url(r'^wish/save/$', views.wish_books_save, name='wish_save'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/save/$', views.register_save, name='register_save'),
    url(r'^list/rent/(?P<pk>\d+)/$', views.rent, name='rent'),
    url(r'^return/(?P<pk>\d+)/$', views.return_book, name='return_book'),
]