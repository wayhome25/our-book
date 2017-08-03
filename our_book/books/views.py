import csv
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.views.generic.dates import MonthArchiveView
from django.views.generic.list import ListView

from .api import get_book_info, register_book
from .models import Book, WishBook


class BookListView(ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'books'


def export_all_books_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'

    writer = csv.writer(response)
    fields = [field.name for field in Book._meta.fields if field.name not in ['rent_info']]
    writer.writerow(fields)
    books = Book.objects.all().values_list(*fields)

    for book in books:
        writer.writerow(book)

    return response


class WishBooksMonthArchiveView(MonthArchiveView):
    model = WishBook
    date_field = "created_at"
    context_object_name = 'wish_books'

    def get_context_data(self, **kwargs):
        context = super(WishBooksMonthArchiveView, self).get_context_data(**kwargs)
        year = self.kwargs['year']
        month = self.kwargs['month']
        context['total_price'] = WishBook.get_total_price(year, month)
        return context


@login_required
def wish_books_save(request):
    if request.method == 'POST':
        isbn = request.POST['isbn']
        message, book = register_book(isbn, model=WishBook)
        messages.info(request, message)
        if book:
            book.wish_user = request.user
            book.save()
        return redirect('books:wish_month', year=datetime.datetime.today().year, month=datetime.datetime.today().month)
    else:
        return redirect('books:wish_month', year=datetime.datetime.today().year, month=datetime.datetime.today().month)


def register(request):
    return render(request, 'books/register.html')


@require_POST
def register_save(request):
    isbn = request.POST['isbn']
    message, book = register_book(isbn)
    messages.info(request, message)
    return redirect('books:register')


@login_required
def rent(request, pk):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=pk)
        book.rent_book(request.user)
        messages.info(request, '대여성공! 반납 예정일은 {} 입니다.'.format(book.rent_info.rent_end))
        return redirect('mybook')
    else:
        return redirect('books:list')


@login_required
@require_POST
def return_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.rent_info.user == request.user:
        book.return_book()
        messages.info(request, '반납성공!')
    else:
        messages.error(request, '문제가 발생했습니다.')
    return redirect('mybook')


def search_result(request):
    if request.GET.get('keyword_list'): # note: 찾는 Key가 없으면 default 값 리턴 (None), KeyError 발생 방지
        keyword = request.GET['keyword_list']
        books = Book.objects.filter(title__icontains=keyword)
        return render(request, 'books/book_list.html', {'books': books})

    if request.GET.get('keyword_wish'):
        keyword = request.GET['keyword_wish']
        books = get_book_info(keyword, display='5')
        return render(request, 'books/wish_book.html', {'books': books})

    if request.GET.get('keyword_register'):
        keyword = request.GET['keyword_register']
        books = get_book_info(keyword, display='5')
        return render(request, 'books/register.html', {'books': books})

    messages.warning(request, '검색어를 입력해주세요.')
    return redirect('books:list')