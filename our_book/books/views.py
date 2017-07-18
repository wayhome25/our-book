from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from .api import get_book_info, register_book
from .models import Book


def list(request):
    if request.method == 'POST':
        keyword = request.POST['keyword-list']
        books = Book.objects.filter(title__icontains=keyword)
    else:
        books = Book.objects.all()
    return render(request, 'books/list.html', {'books': books})


def puchase(request):
    if request.method == 'POST':
        keyword = request.POST['keyword-puchase']
        books = get_book_info(keyword, display='5')
        return render(request, 'books/purchase.html', {'books': books})
    else:
        return render(request, 'books/purchase.html')


def register(request):
    if request.method == 'POST':
        keyword = request.POST['keyword-register']
        books = get_book_info(keyword, display='5')
        return render(request, 'books/register.html', {'books': books})
    else:
        return render(request, 'books/register.html')


@require_POST
def register_save(request):
    isbn = request.POST['isbn']
    result = register_book(isbn)
    messages.info(request, result)
    return redirect('books:register')


@require_POST
def rent(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not book.rent_user:
        book.rent_book(request.user)
        messages.info(request, '대여성공! 반납 예정일은 {} 입니다.'.format(book.rent_end.date()))
    else:
        messages.info(request, '현재 대여중인 도서입니다.')
    return redirect('books:list')
