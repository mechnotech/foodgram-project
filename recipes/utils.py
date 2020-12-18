from recipes.models import Recipe, Ingredient, Tag


def filter_tag(request, tags, recipes_list=None):
    if request.GET.getlist('tags'):
        tags = Tag.objects.filter(slug__in=request.GET.getlist('tags'))
    if recipes_list:
        recipes_list = recipes_list.prefetch_related(
            'author', 'tags'
        ).filter(
            tags__in=tags
        ).distinct()
        return recipes_list
    recipes_list = Recipe.objects.prefetch_related(
        'author', 'tags'
    ).filter(
        tags__in=tags
    ).distinct()
    return recipes_list


def insert_tags(request_data):
    tags = []
    tags_set = Tag.objects.all()
    for tag in tags_set:
        if request_data.get(tag.slug):
            tags.append(tag)
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


def ingredients_check(ingredients):
    max_value = 25000
    error = False
    if not ingredients:
        error = 'Добавьте хотя бы один ингредиент'
    for _, i in ingredients:
        try:
            _ == int(i)
        except ValueError:
            error = 'Количество - только целые положительные числа'
            break
        if int(i) <= 0:
            error = 'Количество не может быть нулевым или отрицательным'
            break
        if int(i) > max_value:
            error = 'Количество слишком большое (нужно не больше 25000)'
            break
    return error
