from django.contrib import admin
from .models import Recipe, Tag, Ingredient, Quantity

class QuantityInline(admin.TabularInline):
    model = Quantity
    min_num = 1
    extra = 0
    verbose_name = 'ингредиент'

class RecipeAdmin(admin.ModelAdmin):
    inlines = (QuantityInline,)
    list_display = ('pk', 'title', 'get_tags', 'get_ingredients', 'prepare_time', 'description', 'pub_date')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tag')


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)