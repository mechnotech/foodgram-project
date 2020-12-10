from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profiles/<username>/', views.profile, name='profile'),
    path('favorite/', views.favorite, name='favorite'),
    path('shop/', views.shop, name='shop'),
    path('shop/downloads/', views.downloads, name='downloads'),
    path('recipes/new/', views.new_recipe, name='new_recipe'),
    path('recipes/<int:recipe_id>', views.recipe, name='recipe'),
    path('recipes/<int:recipe_id>/edit/',
         views.recipe_edit,
         name='recipe_edit'),
    path('recipes/<int:recipe_id>/delete/',
         views.recipe_delete,
         name='recipe_delete'),
    path('follow/', views.my_follow, name='my_follow'),
]
