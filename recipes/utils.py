from recipes.models import Recipe, Ingredient


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


def insert_tags(request_data):
    tags = ''
    if request_data.get('breakfast'):
        tags += 'b'
    if request_data.get('lunch'):
        tags += 'l'
    if request_data.get('dinner'):
        tags += 'd'
    return tags


def insert_ingredients(request_data):
    ingredients = []

    filtered = [
        request_data[key]
        for key in request_data.keys()
        if
        key.startswith('nameIngredient')
        or key.startswith('valueIngredient')
        or key.startswith('unitsIngredient')
    ]

    ing = [filtered[i:i + 3] for i in range(0, len(filtered), 3)]

    for i in ing:
        obj, created = Ingredient.objects.get_or_create(title=i[0],
                                                        dimension=i[2])
        ingredients.append((obj, i[1]))

    return ingredients


def shop_list_text(recipes):
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
