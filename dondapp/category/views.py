import json

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render

from dondapp import models
from dondapp.router import Resource


def page(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed("Only GET requests supported")

    return render(request, 'dondapp/category.html')


class CategoryView(Resource):
    """View for handling category requests"""

    def get(self, request, id=None):
        if id is not None:
            category = get_object_or_404(models.Category, id=id)
            return HttpResponse(category.to_json(), status=200, content_type='application/json')
        else:
            data = []
            for cat in models.Category.objects.all():
                data.append(cat.to_dict())
            return HttpResponse(json.dumps(data), status=200, content_type='application/json')
