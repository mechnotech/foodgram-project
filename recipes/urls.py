from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profiles/<username>/', views.profile, name='profile'),
    path('recipes/<int:recipe_id>', views.recipe, name='recipe'),
    path('follow/', views.my_follow, name='my_follow'),
    path('recipes/<int:recipe_id>/follow/',
         views.follow,
         name='follow'),
    path('recipes/<int:recipe_id>/unfollow/',
         views.unfollow,
         name='unfollow'),
]