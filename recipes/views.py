from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Recipe, User


def get_paginated_view(request, recipe_list, page_size=6):
    paginator = Paginator(recipe_list, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator


def index(request):
    recipes_list = Recipe.objects.all()
    page, paginator = get_paginated_view(request, recipes_list)
    return render(request, 'indexNotAuth.html',
                  {'page': page, 'paginator': paginator})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes_list = author.recipes.all()
    page, paginator = get_paginated_view(request, recipes_list)
    return render(request, 'authorRecipe.html',
                  {'page': page, 'paginator': paginator,
                   'author': author})
