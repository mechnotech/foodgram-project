from recipes.models import Recipe


def filter_tag(request, recipes_list=None):
    tags = request.GET.get('tags', 'bld')
    if recipes_list:
        recipes_list = recipes_list.prefetch_related(
            'author', 'tags'
        ).filter(
            tags__slug__in=tags
        ).distinct()
        return recipes_list, tags
    recipes_list = Recipe.objects.prefetch_related(
        'author', 'tags'
    ).filter(
        tags__slug__in=tags
    ).distinct()
    return recipes_list, tags
