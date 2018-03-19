import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404, render

from dondapp import models
from .router import Resource, auth_required


class HomeView(Resource):
    """View for handling index/home requests"""

    def get(self, request):
        return render(request, 'dondapp/home.html')


class AboutView(Resource):
    """View for handling about requests"""

    def get(self, request):
        return render(request, 'dondapp/about.html')


class FailedView(Resource):
    def get(self, request):
        return render(request, 'dondapp/failed.html')


class LoginView(Resource):
    """View for handling login requests"""

    def post(self, request):
        if "username" not in request.POST:
            return HttpResponseBadRequest("No username given")
        if "password" not in request.POST:
            return HttpResponseBadRequest("No password given")

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return redirect("failed")

    @auth_required
    def delete(self, request):
        return logout(request)


class VoteView(Resource):
    """View for handling voting"""

    @auth_required
    def post(self, request):
        """
        Adds an upvote or downvote to the deal in the request
        :param request: HTTP POST request
        :exception Throws Http404 if the given deal doesn't exist
        :return: Returns HttpReponseBadRequest if either no deal or vote is specified. Returns HttpResponse with HTTP
        OK status if the deal's votes are successfully modified
        """

        data = json.loads(request.body)
        deal = get_object_or_404(models.Deal, id=data['deal_id'])
        if data['upvote']:
            deal.upvotes += 1
        else:
            deal.downvotes += 1

        deal.save()
        return HttpResponse(status=200)

    def get(self, request):
        """
        Returns the upvote and downvote values of the deal specified in the given request
        :param request: HTTP Get request
        :exception Throws Http404 if the given deal doesn't exist
        :return: Returns HttpResponseBadRequest if no deal is specified or HttpResponse with HTTP OK status and the
        following JSON body:
        {
            'upvotes': upvotes as int,
            'downvotes': downvotes as int
        }
        """

        if "deal_id" not in request.GET:
            return HttpResponseBadRequest("No deal specified")
        deal_id = request.GET["deal_id"]
        deal = get_object_or_404(models.Deal, id=deal_id)
        response_data = {
            'upvotes': deal.upvotes,
            'downvotes': deal.downvotes
        }
        return HttpResponse(json.dumps(response_data), status=200, content_type='application/json')
