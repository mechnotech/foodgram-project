from django.forms import ModelForm


from .models import Recipe, Quantity, Ingredient

# from django.forms.models import BaseInlineFormSet
# from django.forms.models import inlineformset_factory
#
# class BaseIngredientFormSet(BaseInlineFormSet):
#     def add_fields(self, form, index):
#
#         super(BaseIngredientFormSet, self).add_fields(form, index)
#
# ChildrenFormset = inlineformset_factory(Quantity,
#                                         Ingredient,
#                                         formset=BaseIngredientFormSet,
#                                         extra=1)
# class QuantityInline(django.forms.metaclass=):
#     model = Quantity
#     min_num = 1
#     extra = 0
#     verbose_name = 'ингредиент'

# class RecipeForm(ModelForm):
#
#
#     class Meta:
#         model = Recipe
#         fields = ('title', 'tags', 'ingredients', 'description', 'prepare_time')