from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # note 자동 로그인
            return redirect('login')  # fixme 차후에 root 경로로 변경할 것
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})