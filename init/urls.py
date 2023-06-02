from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('tasks/dashboard/', views.dashboard, name='dashboard'),
    path('safeguards/', views.safeguard, name='safeguard'),
    path('month/',views.monthly_report,name='month'),
    path('register/', views.register, name='register'),
    path('',views.register,name='register'),
    path('index/',views.index,name='index'),
]
