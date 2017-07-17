from django.shortcuts import render

from .api import get_book_info


def puchase(request):
    if request.method == 'POST':
        keyword = request.POST['keyword-puchase']
        books = get_book_info(keyword, display='5')
        return render(request, 'books/purchase.html', {'books': books})
    else:
        return render(request, 'books/purchase.html')