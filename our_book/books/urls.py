from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list/$', views.BookListView.as_view(), name='list'),
    url(r'^list/export/csv/$', views.export_all_books_csv, name='export_all_books_csv'),
    url(r'^wish/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
        views.WishBooksMonthArchiveView.as_view(month_format='%m'),
        name='wish_month'),
    url(r'^wish/save/$', views.wish_books_save, name='wish_save'),
    url(r'^wish/(?P<pk>\d+)/cancel/$', views.cancel_wish_book, name='wish_cancel'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/save/$', views.register_save, name='register_save'),
    url(r'^list/rent/(?P<pk>\d+)/$', views.rent, name='rent'),
    url(r'^return/(?P<pk>\d+)/$', views.return_book, name='return_book'),
    url(r'^search/result/$', views.search_result, name='search_result'),
]