"""
URL configuration for workshopdjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.room_list, name='room_list'),
    path('add/', views.room_add, name='room_add'),
    path('room/new/', views.room_add, name='room_add'),
    path('room/delete/<int:id>/', views.room_delete, name='room_delete'),
    path('room/edit/<int:id>/', views.room_edit, name='room_edit'),
    path('room/reserve/<int:id>/', views.room_reserve, name='room_reserve'),
    path('room/<int:id>/', views.room_detail, name='room_detail'),
]
