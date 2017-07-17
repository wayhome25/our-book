from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .api import get_book_info, register_book


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
    return redirect('book:register')

