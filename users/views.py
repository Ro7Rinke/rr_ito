from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm
from .forms import UserLoginForm
from django.contrib import messages
from .email import send_password_reset_email
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import User, PasswordResetToken
from django.contrib.auth.hashers import make_password

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o usuário no banco de dados
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}! Faça login para continuar.')
            return redirect('login')  # Redireciona para a página de login após o cadastro
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                return redirect('dashboard')  # Redireciona para a página de dashboard após o login
            else:
                messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def send_password_reset_email_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            token = get_random_string(length=32)
            reset_url = request.build_absolute_uri(f'/users/reset_password/{token}/')

            PasswordResetToken.objects.create(user=user, token=token)
            send_password_reset_email(email, reset_url)
            return render(request, 'users/password_reset_email_sent.html')
        except User.DoesNotExist:
            return render(request, 'users/password_reset_email_not_found.html')
    return render(request, 'users/password_reset_email_form.html')

def reset_password_view(request, token):
    token_obj = get_object_or_404(PasswordResetToken, token=token)
    if not token_obj.is_valid():
        return render(request, 'users/password_reset_token_invalid.html')

    if request.method == 'POST':
        password = request.POST['password']
        user = token_obj.user
        user.password = make_password(password)
        user.save()
        token_obj.delete()
        return redirect('login')
    return render(request, 'users/reset_password_form.html', {'token': token})

