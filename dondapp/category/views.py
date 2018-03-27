import json

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render

from dondapp import models
from dondapp.router import Resource, authority_required


def page(request):
    """View for handling a get request for the category page"""
    if request.method != 'GET':
        return HttpResponseNotAllowed("Only GET requests supported")

    return render(request, 'dondapp/category.html')


class CategoryView(Resource):
    """View for handling category requests"""

    def get(self, request, id=None, deals=False):
        """
        If id is not given, returns a HttpResponse(200) with a JSON encoded list of all categories. If the id is given
        and deals is True, returns HttpResponse(200) with a JSON encoded list of all deals with the given category id,
        if the id doesn't exist, the JSON list is empty. If the id is given and deals is False, returns a
        HttpResponse(404) if there is no category with the given id, otherwise HttpResponse(200) with the category with
        the given id encoded in JSON.
        :param request: HTTP GET Request
        :param id: Category ID
        :param deals: Get deals or just category info
        :return: HttpResponse(404), HttpResponse(200)
        """
        if id is not None:
            if deals:
                deals = models.Deal.objects.all().filter(category_id=id)
                data = []
                for deal in deals:
                    data.append(deal.to_dict())
                return HttpResponse(json.dumps(data), status=200, content_type='application/json')
            else:
                try:
                    category = models.Category.objects.get(id=id)
                except models.Category.DoesNotExist:
                    return HttpResponse('Category not found', status=200)
                return HttpResponse(category.to_json(), status=200, content_type='application/json')
        else:
            data = []
            for cat in models.Category.objects.all():
                data.append(cat.to_dict())
            return HttpResponse(json.dumps(data), status=200, content_type='application/json')

    @authority_required
    def post(self, request):
        """
        Creates a new category based on the POST data in the given request. This can only be done by superusers.
        :param request: HTTP POST request
        :return: Returns HttpResponse(401) if the user is not logged in, HttpResponseForbidden if the user is not a
        superuser, otherwise HttpResponse(200)
        """
        for attr in models.Category.REQUIRED:
            if attr not in request.POST:
                return HttpResponseBadRequest(attr + " is required")

        cat = models.Category(id=request.POST["id"], name=request.POST['name'], description=request.POST['description'])
        cat.save()
        return HttpResponse(status=200)

    @authority_required
    def delete(self, request, id):
        """
        Deletes the category with the given id.
        :param request: HTTP DELETE Request
        :param id: Id of category to delete
        :return: Returns HttpResponse(200)
        """
        models.Category.objects.get(id=id).delete()
        return HttpResponse(status=200)
