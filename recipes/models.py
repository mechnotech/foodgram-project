from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    color = models.CharField(max_length=10, blank=True, null=True, )
    tag = models.CharField(max_length=10, blank=False, null=False, )
    slug = models.SlugField(max_length=1, blank=True, null=True, )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tag', 'color'],
                                    name='tags_color_pairs')
        ]

    def __str__(self):
        return self.tag


class Ingredient(models.Model):
    title = models.CharField('Название инградиента', max_length=150,
                             blank=False, unique=False)
    dimension = models.CharField('Мера измерения', max_length=10,
                                 blank=True)

    class Meta:
        ordering = [models.F('title').asc()]
        verbose_name_plural = 'Ингредиенты'
        verbose_name = 'Ингредиент'

    def __str__(self):
        return f'{self.title} ({self.dimension})'


class Recipe(models.Model):
    title = models.CharField(
        'Название рецепта',
        max_length=200,
        unique=True,
        help_text='Название рецепта (не более 200 символов)',
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')

    prepare_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        default=10,
        help_text='Время приготовления в минутах',
    )

    description = models.TextField('Описание рецепта', max_length=2500)
    ingredients = models.ManyToManyField(Ingredient,
                                         through='Quantity',
                                         related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    pub_date = models.DateTimeField('Время создания рецепта',
                                    auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепт'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_tags(self):
        return self.tags.only('tag')

    def render_tags(self):
        return self.tags.only('tag', 'color')

    def get_tags_slug(self):
        tag = ''
        for t in self.tags.only('slug'):
            tag += t.slug
        return tag

    def get_ingredients(self):
        ingredients = []
        for i in self.quantity_set.only(
                'ingredient',
                'value',
                'ingredient__dimension'):

            ingredients.append((i.ingredient, i.value))

        return ingredients

    def __str__(self):
        return self.title


class Quantity(models.Model):
    value = models.PositiveSmallIntegerField('Количество инградиента')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ingredient} - {self.value}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorite_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_favorites')

    def __str__(self):
        return f'{self.recipe.title} избранный пользователем {self.user}'


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shopcart_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_shopcarts')

    def __str__(self):
        return f'{self.recipe.title} в покупках пользователя {self.user}'


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='user_follow')
        ]
        verbose_name_plural = 'Подписки'
        verbose_name = 'Подписка'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


def is_following(self, author):
    """Проверка есть ли подписка пользователя на автора"""
    return self.follower.filter(author=author).exists()


def favorites_list(self):
    """Вернуть список всех, избранных пользователем, рецептов"""
    qs = self.favorite_recipes.filter(user=self)
    recipes_ids = qs.values_list('recipe', flat=True)
    return Recipe.objects.filter(pk__in=recipes_ids)


def shop_cart_list(self):
    """Вернуть список всех покупок пользователя"""
    qs = self.shopcart_recipes.filter(user=self)
    recipes_ids = qs.values_list('recipe', flat=True)
    return Recipe.objects.filter(pk__in=recipes_ids)


def shop_count(self):
    """Количество покупок пользователя"""
    return len(self.shopcart_recipes.filter(user=self))


User.add_to_class('is_following', is_following)
User.add_to_class('favorites_list', favorites_list)
User.add_to_class('shop_cart_list', shop_cart_list)
User.add_to_class('shop_count', shop_count)
