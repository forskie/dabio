from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm
from .models import CustomUser


def register(request):
    # Обработка регистрации пользователя
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Используйте 'django.contrib.auth.backends.ModelBackend' для явного входа
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('user:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})
    

def login_view(request):
    # Обработка входа пользователя
    if request.method == 'POST':
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('user:profile')
    else:
        form = CustomUserLoginForm()
    return render(request, 'user/login.html', {'form': form})


@login_required
def profile_views(request):
    # Отображает страницу профиля
    return render(request, 'user/profile.html', {'user': request.user})


@login_required
def account_details(request):
    # Отображает детали аккаунта. Исправлено имя шаблона на 'user/accounts_detail.html' (множественное число)
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, 'user/accounts_detail.html',
                  {'user': user})


@login_required
def edit_account_details(request):
    # Отображает форму для редактирования деталей аккаунта
    form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'user/edit_account_details.html', 
                  {'user': request.user, 'form': form})


@login_required
def update_account_details(request):
    # Обработка POST-запроса для обновления деталей аккаунта
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.clean()  
            user.save()
            # Успешный POST: возвращает страницу деталей аккаунта (множественное число)
            return render(request, 'user/accounts_detail.html', {'user': user})
        else:
            # Ошибка формы: возвращает страницу редактирования
            return render(request, 'user/edit_account_details.html', {'user': request.user, 'form': form})
            
    # GET-запрос: возвращает страницу деталей аккаунта. Исправлено имя шаблона на 'user/accounts_detail.html' (множественное число)
    return render(request, 'user/accounts_detail.html', {'user': request.user})
     
       
def logout_view(request):
    # Выход из системы
    logout(request)
    return redirect('user:register')