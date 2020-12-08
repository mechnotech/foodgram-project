from django.contrib import admin
from .models import Recipe, Tag, Ingredient, Follow, Favorite, ShopCart


class QuantityInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    verbose_name = 'ингредиент'


class RecipeAdmin(admin.ModelAdmin):
    inlines = (QuantityInline,)

    list_filter = ('title',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tag')


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    search_fields = ('user',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShopCart, ShopCartAdmin)
