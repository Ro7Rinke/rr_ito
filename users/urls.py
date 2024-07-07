from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('send_password_reset_email/', views.send_password_reset_email_view, name='send_password_reset_email'),
    path('reset_password/<str:token>/', views.reset_password_view, name='reset_password'),
]
from users.models import User
