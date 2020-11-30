from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profiles/<username>/', views.profile, name='profile'),
]