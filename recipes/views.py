from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, User, Follow
from .utils import filter_tag


def get_paginated_view(request, recipe_list, page_size=6):
    paginator = Paginator(recipe_list, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator


def index(request):
    recipes_list, tags = filter_tag(request)
    page, paginator = get_paginated_view(request, recipes_list)
    if request.user.is_authenticated:
        return render(request, 'index.html',
                  {'page': page, 'paginator': paginator, 'tags': tags})
    return render(request, 'indexNotAuth.html',
                  {'page': page, 'paginator': paginator, 'tags': tags})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes_list, tags = filter_tag(request)
    recipes_list = recipes_list.filter(author=author)
    page, paginator = get_paginated_view(request, recipes_list)
    return render(request, 'authorRecipe.html',
                  {'page': page,
                   'paginator': paginator,
                   'author': author,
                   'tags': tags})


def recipe(request, recipe_id):
    one_recipe = get_object_or_404(Recipe, pk=recipe_id)
    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=one_recipe.author).exists()
    return render(request, 'singlePage.html',
                  {'recipe': one_recipe, 'following': following}
                  )

def new_recipe(request):
    return render(request, 'formRecipe.html')


def favorite(request):
    return render(request, 'favorite.html')


@login_required
def my_follow(request):
    page_size = 3
    rp_per_card = 4
    authors = Follow.objects.filter(user=request.user).all()
    card_list = []
    for author in authors:
        last_four_recipes = author.author.recipes.all()[:rp_per_card]
        recipe_count = author.author.recipes.count() - rp_per_card
        card_list.append(
            {"author": author,
             "recipes_list": last_four_recipes,
             "count": recipe_count if recipe_count > 0 else 0}
        )
    page, paginator = get_paginated_view(request, card_list, page_size)
    return render(request, 'myFollow.html',
                  {'page': page, 'paginator': paginator})



