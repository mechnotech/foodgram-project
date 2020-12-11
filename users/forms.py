from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField

User = get_user_model()


class CreationForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta(UserCreationForm.Meta):

        model = User
        fields = ('first_name', 'username', 'email')

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email:
            raise forms.ValidationError('Укажите e-mail для регистрации!')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой e-mail уже существует!')
        return email
