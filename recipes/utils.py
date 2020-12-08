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


def get_download_file(recipes):
    ingredients = recipes.values_list(
        'ingredients__title',
        'ingredients__dimension',
        'ingredients__quantity__value'
    ).distinct()
    rd = {}
    file_text = ''

    for i in ingredients:
        if not i[0] is None:
            key = f'{i[0]}@{i[1]}'
            if rd.get(key):
                rd[key] += i[2]
            else:
                rd[key] = i[2]

    for k, v in rd.items():
        file_text += f'{" ".join(k.split("@"))} {v} \n'

    return file_text
