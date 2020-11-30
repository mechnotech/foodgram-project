from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, User, Follow


def get_paginated_view(request, recipe_list, page_size=6):
    paginator = Paginator(recipe_list, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator


def index(request):
    recipes_list = Recipe.objects.all()
    page, paginator = get_paginated_view(request, recipes_list)
    return render(request, 'index.html',
                  {'page': page, 'paginator': paginator})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes_list = author.recipes.all()
    page, paginator = get_paginated_view(request, recipes_list)
    return render(request, 'authorRecipe.html',
                  {'page': page, 'paginator': paginator,
                   'author': author})


def recipe(request, recipe_id):
    one_recipe = get_object_or_404(Recipe, pk=recipe_id)
    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=one_recipe.author).exists()
    return render(request, 'recipe_page.html', {'recipe': one_recipe, 'following': following})


@login_required
def follow_index(request):
    authors = Follow.objects.values_list(
        'author', flat=True).filter(user=request.user).all()
    post_list = Recipe.objects.filter(author__in=authors)
    page, paginator = get_paginated_view(request, post_list)
    return render(request, 'myFollow.html',
                  {'page': page, 'paginator': paginator})


@login_required
def follow(request, recipe_id):
    one_recipe = get_object_or_404(Recipe, pk=recipe_id)
    user = request.user
    author = one_recipe.author
    if user == author:
        return redirect('recipe', recipe_id=recipe_id)
    user.follower.get_or_create(author=author)
    return redirect('recipe', recipe_id=recipe_id)


@login_required
def unfollow(request, recipe_id):
    one_recipe = get_object_or_404(Recipe, pk=recipe_id)
    user = request.user
    author = one_recipe.author
    following = user.follower.filter(author=author)
    following.delete()
    return redirect('recipe', recipe_id=recipe_id)
