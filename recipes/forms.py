from django import forms
from django.core.exceptions import ValidationError
from recipes.models import Recipe, Tag, Ingredient


class RecipeForm(forms.ModelForm):
    # tags = forms.ModelMultipleChoiceField(
    #     queryset=Tag.objects.all(), to_field_name="slug"
    # )
    # ingredients = forms.ModelMultipleChoiceField(
    #     queryset=Ingredient.objects.all(), to_field_name="title"
    # )

    class Meta:
        model = Recipe
        fields = (
            "title",
            "prepare_time",
            "description",
            "image",
        )

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image is None:
            return image
        image_max_size = 4 * 1048576
        if image:
            if image.size > image_max_size:
                raise ValidationError('Картинка слишком большая ( > 4Мб )')
            return image
        return image
