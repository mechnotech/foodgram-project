from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    tag = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return self.tag


class Ingredient(models.Model):
    title = models.CharField('Название инградиента', max_length=150,
                             blank=False, unique=True)
    dimension = models.CharField('Мера измерения', max_length=10,
                                 blank=False)

    class Meta:
        ordering = [models.F('title').asc()]
        verbose_name_plural = 'Ингредиенты'
        verbose_name = 'Ингредиент'

    def __str__(self):
        return self.title


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

    description = models.TextField('Описание рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='Quantity',
                                         related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    pub_date = models.DateTimeField('Время создания рецепта',
                                    auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепт'

    def get_tags(self):
        return self.tags.only('tag')

    def get_ingredients(self):
        return self.quantity.only('ingredient', 'value')

    def __str__(self):
        return self.title


class Quantity(models.Model):
    value = models.PositiveSmallIntegerField('Количество инградиента')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ingredient} - {self.value}'
