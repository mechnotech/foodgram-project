from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Recipe


def get_paginated_view(request, recipe_list, page_size=6):
    paginator = Paginator(recipe_list, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator


def index(request):
    recipe_list = Recipe.objects.all()
    page, paginator = get_paginated_view(request, recipe_list)
    return render(request, 'indexNotAuth.html',
                  {'page': page, 'paginator': paginator})
