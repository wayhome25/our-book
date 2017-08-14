from django.contrib import admin

from .forms import BookForm
from .models import Book, RentHistory, WishBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'publisher', 'price']
    list_display_links = ['title', 'author', 'publisher']
    search_fields = ['title']
    form = BookForm


@admin.register(RentHistory)
class RentHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'rent_start', 'rent_end', 'return_status', 'sent_overdue_email']
    list_display_links = ['user', 'book']


@admin.register(WishBook)
class WishBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'publisher', 'price', 'wish_user']
    list_display_links = ['title', 'author', 'publisher']
    search_fields = ['title']

