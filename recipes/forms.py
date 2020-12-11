from django import forms
from django.core.exceptions import ValidationError

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
        if image is None:
            return image
        image_max_size = 4 * 1048576
        if image:
            if image.size > image_max_size:
                raise ValidationError('Картинка слишком большая ( > 4Мб )')
            return image
        return image
