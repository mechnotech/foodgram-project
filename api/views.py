import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from recipes.models import (
    Ingredient,
    Follow,
    Recipe,
    User,
)


class Ingredients(LoginRequiredMixin, View):


    def get(self, request):
        query = request.GET.get("query", None)
        if query is not None:
            response = Ingredient.objects.filter(title__icontains=query).values(
                "title", "dimension"
            )
            return JsonResponse(list(response), safe=False)
        return JsonResponse({"success": False}, status=400)




class Subscribe(LoginRequiredMixin, View):


    def post(self, request):
        req_ = json.loads(request.body)
        user_id = req_.get("id", None)
        if user_id is not None:

            if self.request.user.id == user_id:
                return JsonResponse({"success": False}, status=403)
            author = get_object_or_404(User, pk=user_id)
            obj, created = Follow.objects.get_or_create(
                user=request.user, author=author
            )
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, author_id):
        following = get_object_or_404(Follow, user=request.user, author=author_id)
        following.delete()
        return JsonResponse({"success": True})


