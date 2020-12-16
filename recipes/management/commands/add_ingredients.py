import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Добавить список ингредиентов в базу'

    def handle(self, *args, **options):
        with open('recipes/presets/ingredients.csv',
                  'r',
                  encoding='utf8'
                  ) as f:
            reader = csv.reader(f)
            current = Ingredient.objects.count()
            for row in reader:
                title, dimention = row
                Ingredient.objects.get_or_create(
                    title=title,
                    dimension=dimention
                )
            result = Ingredient.objects.count() - current
            print(f'В базу добавлено {result} ингредиентов')
