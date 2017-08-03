from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .forms import SignupForm
from books.models import Book


User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # note 자동 로그인
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'accounts/profile.html', {'user': user})


@login_required
def mybook(request):
    books = request.user.get_rent_books()
    return render(request, 'accounts/mybook.html', {'books': books})