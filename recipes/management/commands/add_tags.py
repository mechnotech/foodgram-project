import csv

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Добавить список тэгов в базу (цвет и наименование)'

    def handle(self, *args, **options):
        with open('recipes/presets/tags.csv',
                  'r',
                  encoding='utf8'
                  ) as f:
            reader = csv.reader(f)
            current = Tag.objects.count()
            for row in reader:
                color, tag, slug = row
                Tag.objects.get_or_create(
                    color=color,
                    tag=tag,
                    slug=slug
                )
            result = Tag.objects.count() - current
            print(f'В базу добавлено {result} тэгов')
