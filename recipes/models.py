from django.db import models
from django.urls import reverse


class Tag(models.Model):
    tag = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return self.tag


class Ingredient(models.Model):
    title = models.CharField('Название инградиента', max_length=150,
                             blank=False, unique=True)
    dimension = models.CharField('Мера измерения', max_length=10,
                                 blank=False)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(
        'Название рецепта',
        max_length=200,
        unique=True,
        help_text='Название рецепта (не более 200 символов)',
    )

    prepare_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        default=10,
        help_text='Время приготовления в минутах',
    )

    description = models.TextField('Описание рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='Quantity', related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    pub_date = models.DateTimeField('Время создания рецепта',
                                      auto_now_add=True)

    def get_tags(self):
        return ",".join([str(t) for t in self.tags.all()])

    def get_ingredients(self):
        return self.quantity_set.only('ingredient', 'value')

    def __str__(self):
        return self.title


class Quantity(models.Model):
    value = models.PositiveSmallIntegerField('Количество инградиента')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ingredient} - {self.value}'