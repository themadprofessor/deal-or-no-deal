import json

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render

from dondapp import models
from dondapp.router import Resource, authority_required


def page(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed("Only GET requests supported")

    return render(request, 'dondapp/category.html')


class CategoryView(Resource):
    """View for handling category requests"""

    def get(self, request, id=None, deals=False):
        if id is not None:
            if deals:
                deals = models.Deal.objects.get(category_id=id)
                data = []
                for deal in deals:
                    data.append(deal.to_dict())
                return HttpResponse(json.dumps(data), status=200, content_type='application/json')
            else:
                category = get_object_or_404(models.Category, id=id)
                return HttpResponse(category.to_json(), status=200, content_type='application/json')
        else:
            data = []
            for cat in models.Category.objects.all():
                data.append(cat.to_dict())
            return HttpResponse(json.dumps(data), status=200, content_type='application/json')

    @authority_required
    def post(self, request):
        for attr in models.Category.REQUIRED:
            if attr not in request.POST:
                return HttpResponseBadRequest(attr + " is required")

        cat = models.Category(id=request.POST["id"], name=request.POST['name'], description=request.POST['description'])
        cat.save()
        return HttpResponse(status=200)

    def delete(self, request, id):
        models.Category.objects.get(id=id).delete()
        return HttpResponse(status=200)
