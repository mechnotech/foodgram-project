from django.urls import path
from . import views

urlpatterns = [
    path("ingredients/", views.Ingredients.as_view()),
    path("subscriptions/", views.Subscribe.as_view()),
    path("subscriptions/<int:author_id>", views.Subscribe.as_view()),
]
