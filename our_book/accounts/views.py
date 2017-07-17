from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import SignupForm


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
