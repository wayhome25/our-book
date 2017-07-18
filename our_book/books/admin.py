from django.contrib import admin
from .models import Book, WishBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'price']
    list_display_links = ['title', 'author', 'publisher']
    search_fields = ['title']


@admin.register(WishBook)
class WishBookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'price']
    list_display_links = ['title', 'author', 'publisher']
    search_fields = ['title']

