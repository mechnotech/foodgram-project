from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profiles/<username>/', views.profile, name='profile'),
    path('favorite/', views.favorite, name='favorite'),
    path('recipes/new/', views.new_recipe, name='new_recipe'),
    path('recipes/<int:recipe_id>', views.recipe, name='recipe'),
    path('follow/', views.my_follow, name='my_follow'),
]