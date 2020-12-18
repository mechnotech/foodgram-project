from django import forms
from django.core.exceptions import ValidationError

from foodgram.settings import IMAGE_MAX_SIZE
from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    tags = forms.BooleanField(required=False)
    ingredients = forms.BooleanField(required=False)

    class Meta:
        model = Recipe
        fields = (
            'title',
            'prepare_time',
            'description',
            'image',
            'tags',
            'ingredients',
        )

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError('Добавьте картинку готового блюда')

        if image:
            if image.size > IMAGE_MAX_SIZE:
                raise ValidationError('Картинка слишком большая ( > 4Мб )')
            return image
        return image
