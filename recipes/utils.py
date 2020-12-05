from recipes.models import Recipe


def filter_tag(request):
    tags = request.GET.get('tags', 'bld')

    recipes_list = Recipe.objects.prefetch_related(
        'author', 'tags'
    ).filter(
        tags__slug__in=tags
             ).distinct()
    return recipes_list, tags
