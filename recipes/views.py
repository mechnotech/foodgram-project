from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import requires_csrf_token

from foodgram.settings import (
    SHOP_LIST_FILENAME,
    RECIPE_PER_FOLLOW_CARD,
    FOLLOW_PAGE_SIZE,
    DEFAULT_PAGE_SIZE
)
from .forms import RecipeForm
from .models import Recipe, User, Follow, Tag, Quantity
from .utils import (
    filter_tag,
    shop_list_text,
    insert_tags,
    insert_ingredients,
    ingredients_check,
)


def get_paginated_view(request, recipe_list, page_size=DEFAULT_PAGE_SIZE):
    paginator = Paginator(recipe_list, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator


def index(request):
    tags = Tag.objects.all()
    recipes_list = filter_tag(request, tags=tags)
    page, paginator = get_paginated_view(request, recipes_list)
    if request.user.is_authenticated:
        return render(request, 'indexAuth.html',
                      {'page': page,
                       'paginator': paginator,
                       'tags': tags,
                       }
                      )
    return render(request, 'indexNotAuth.html',
                  {'page': page, 'paginator': paginator, 'tags': tags})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    tags = Tag.objects.all()
    recipes_list = filter_tag(request, tags=tags)
    recipes_list = recipes_list.filter(author=author)
    page, paginator = get_paginated_view(request, recipes_list)
    return render(request, 'authorRecipe.html',
                  {'page': page,
                   'paginator': paginator,
                   'author': author,
                   'tags': tags}
                  )


@login_required
def favorite(request):
    tags = Tag.objects.all()
    user = request.user
    favorites = user.favorites_list()
    if not favorites:
        return render(request, 'favorite.html', {'tags': tags})
    recipes_list = filter_tag(request, tags=tags, recipes_list=favorites)
    page, paginator = get_paginated_view(request, recipes_list)
    return render(request, 'favorite.html',
                  {'page': page,
                   'paginator': paginator,
                   'tags': tags,
                   }
                  )


def recipe(request, recipe_id):
    one_recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'singlePage.html', {'recipe': one_recipe, })


@login_required
def new_recipe(request):
    tags_set = Tag.objects.all
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        tags = insert_tags(request.POST)
        ingredients = insert_ingredients(request.POST)
        ingredients_errors = ingredients_check(ingredients)
        if not tags:
            form.add_error('tags', 'Определите хотя бы один тэг')
        if ingredients_errors:
            form.add_error('ingredients', ingredients_errors)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.pub_date = timezone.now()
            recipe.save()

            tags = insert_tags(request.POST)
            for i in ingredients:
                Quantity.objects.get_or_create(
                    ingredient=i[0],
                    value=i[1],
                    recipe=recipe
                )
            recipe.tags.set(tags)

            return redirect('recipe', recipe_id=recipe.pk)
    else:
        form = RecipeForm(request.POST or None)
        tags = get_object_or_404(Tag, pk=1)
        ingredients = None
    return render(request, 'formRecipe.html',
                  {'form': form,
                   'tags': tags,
                   'tags_set': tags_set,
                   'ingredients': ingredients}
                  )


@login_required
def recipe_edit(request, recipe_id):
    tags_set = Tag.objects.all
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe', recipe_id=recipe_id)

    if request.method == 'POST':
        form = RecipeForm(request.POST or None,
                          files=request.FILES or None, instance=recipe)
        tags = insert_tags(request.POST)
        ingredients = insert_ingredients(request.POST)
        ingredients_errors = ingredients_check(ingredients)
        if not tags:
            form.add_error('tags', 'Определите хотя бы один тэг')
        if ingredients_errors:
            form.add_error('ingredients', ingredients_errors)

        if form.is_valid():
            recipe.ingredients.clear()
            recipe.tags.remove()

            for i in ingredients:
                Quantity.objects.get_or_create(
                    ingredient=i[0],
                    value=i[1],
                    recipe=recipe
                )
            recipe.tags.set(tags)
            recipe.save()

            return redirect('recipe', recipe_id=recipe_id)
    else:
        tags = recipe.tags.all()
        form = RecipeForm(instance=recipe)
        ingredients = recipe.get_ingredients()
    return render(
        request, 'formChangeRecipe.html',
        {'form': form, 'recipe': recipe, 'tags': tags, 'tags_set': tags_set,
         'ingredients': ingredients})


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
        return redirect('profile', username=request.user.username)
    return redirect('recipe', recipe_id=recipe_id)


@login_required
def my_follow(request):
    page_size = FOLLOW_PAGE_SIZE
    rp_per_card = RECIPE_PER_FOLLOW_CARD
    authors = Follow.objects.filter(user=request.user).all()
    card_list = []
    for author in authors:
        last_recipes = author.author.recipes.all()[:rp_per_card]
        recipe_count = author.author.recipes.count() - rp_per_card
        card_list.append(
            {"author": author,
             "recipes_list": last_recipes,
             "count": recipe_count if recipe_count > 0 else 0}
        )
    page, paginator = get_paginated_view(request, card_list, page_size)
    return render(request, 'myFollow.html',
                  {'page': page, 'paginator': paginator})


@login_required
def shop(request):
    return render(request, 'shopList.html')


@login_required
def downloads(request):
    recipes = request.user.shop_cart_list()
    file_text = shop_list_text(recipes)

    response = HttpResponse(file_text,
                            content_type='application/text charset=utf-8'
                            )
    response['Content-Disposition'] = 'attachment;'
    response['Content-Disposition'] += f' filename="{SHOP_LIST_FILENAME}"'
    return response


@requires_csrf_token
def page_bad_request(request, exception):
    return render(request, "misc/400.html", {"path": request.path}, status=400)


@requires_csrf_token
def page_not_found(request, exception):
    return render(request, 'misc/404.html', {"path": request.path}, status=404)


@requires_csrf_token
def server_error(request):
    return render(request, "misc/500.html", status=500)
