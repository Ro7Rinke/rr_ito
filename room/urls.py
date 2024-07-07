from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.room_list, name='room_list'),
]
