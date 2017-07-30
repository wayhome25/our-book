from django.contrib import admin
from .models import Book, RentHistory, WishBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'price']
    list_display_links = ['title', 'author', 'publisher']
    search_fields = ['title']


@admin.register(RentHistory)
class RentHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'rent_start', 'rent_end', 'return_status']
    list_display_links = ['user', 'book']


@admin.register(WishBook)
class WishBookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'price']
    list_display_links = ['title', 'author', 'publisher']
    search_fields = ['title']

