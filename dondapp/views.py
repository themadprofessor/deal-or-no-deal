import json

import datetime

import pytz
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.shortcuts import render as django_render

from dondapp import models
from .router import Resource, auth_required


def render(request, *args, **kwargs):
    """Wrapper for django's render function which ensures there is a list of categories in the context if the user is
    logged in"""
    if request.user.is_authenticated:
        context = kwargs.get('context', {})
        if 'categories' not in context:
            context['categories'] = models.Category.objects.all()
            kwargs['context'] = context
    return django_render(request, *args, **kwargs)


class HomeView(Resource):
    """View for handling index/home requests"""

    def get(self, request):
        """
        Returns the home page
        :param request: HTTP GET Request
        :return: returns the home page
        """
        return render(request, 'dondapp/home.html')


class AboutView(Resource):
    """View for handling about requests"""

    def get(self, request):
        """
        Returns the about page
        :param request: HTTP GET Request
        :return: returns the about page
        """
        return render(request, 'dondapp/about.html')


class FailedView(Resource):
    """View for handling failed credential requests"""
    def get(self, request):
        """
        Returns the failed credentials page
        :param request: HTTP GET Request
        :return: returns the failed credentials page
        """
        return render(request, 'dondapp/failed.html')


class SearchView(Resource):
    """View for handling search queries"""
    def get(self, request):
        """Searches for deals which match the given query
        :param request: HTTP GET Request
        :return Returns HttpResponseBadRequest if there is no query in the GET data, otherwise returns the search page
        with all deals which match the query.
        """
        if 'query' not in request.GET:
            return HttpResponseBadRequest("No query given")
        query = request.GET['query']
        data = {
            # Q allows for complex queries, this is equivalent to:
            # SELECT * FROM dondapp_deal WHERE title LIKE %query% OR description LIKE %query%;
            'deals': models.Deal.objects.filter(Q(title__contains=query) | Q(description__contains=query)),
            'query': query
        }
        return render(request, 'dondapp/search.html', context=data)


class DealView(Resource):
    """View for creating and viewing deals"""
    def get(self, request, id=None):
        """
        View a deal's page.
        :param request: HTTP GET Request
        :param id: ID of deal to view.
        :return: Returns HttpResponse(404) if there is no deal with the given ID, otherwise return the deal's page.
        """
        try:
            deal = models.Deal.objects.get(id=id)
        except models.Deal.DoesNotExist:
            return HttpResponse('Deal not found', status=404)
        context = {
            'deal': deal,
            'comments': models.Comment.objects.filter(deal_id=id),
            'upvoted': deal.upvoters.filter(username=request.user.username).exists(),
            'downvoted': deal.downvoters.filter(username=request.user.username).exists()
        }
        return render(request, 'dondapp/deal.html', context=context)

    def post(self, request):
        """
        Create a new deal with the POST data in the given request.
        :param request: HTTP POST Request
        :return: Returns HttpResponseBadRequest if an attribute required to create deal is missing from the POST data,
        HttpResponse(404) if either the user_id or category_id don't exist, otherwise returns HttpResponse(200).
        """
        for required in models.Deal.REQUIRED:
            if required not in request.POST:
                return HttpResponseBadRequest(required + ' not specified')

        if not models.Category.objects.filter(id=request.POST['category_id']).exists():
            return HttpResponse('Category not found', status=404)
        if not models.User.objects.filter(username=request.POST['user_id']).exists():
            return HttpResponse('User not found', status=404)

        deal = models.Deal(category_id=models.Category.objects.get(id=request.POST['category_id']), user_id=models.User.objects.get(username=request.POST['user_id']),
                           title=request.POST['title'], description=request.POST['description'],
                           price=request.POST['price'])
        deal.save()
        deal.upvoters.filter(username=request.user.username).exists()
        return HttpResponse(status=200)


class NewDealView(Resource):
    """View for getting all deals sorted by creation date"""
    def get(self, request):
        """
        Get all deals sorted by number of creation date.
        :param request: HTTP GET Request
        :return: Returns HttpResponse(200) with a JSON encoded list of all deals sorted by creation date.
        """
        deals = models.Deal.objects.all()
        data = []
        for deal in deals:
            data.append(deal.to_dict())
        data = sorted(data, key=lambda x:x["creation_date"])
        return HttpResponse(json.dumps(data), status=200, content_type="application/json")
        
        
class TopDealView(Resource):
    """View for getting all deals sorted by number of upvotes"""
    def get(self, request):
        """
        Get all deals sorted by number of upvotes.
        :param request: HTTP GET Request
        :return: Returns HttpResponse(200) with a JSON encoded list of all deals sorted by upvotes.
        """
        deals = models.Deal.objects.all()
        data = []
        for deal in deals:
            data.append(deal.to_dict())
        data = sorted(data, key=lambda x:x["upvotes"],reverse=True)
        return HttpResponse(json.dumps(data), status=200, content_type="application/json")


class CommentView(Resource):
    """View for creating, viewing and deleting comments"""

    def get(self, request):
        """
        Returns the JSON encoded form of the comment with the ID specified in the GET request's data.
        :param request: HTTP GET Request
        :return: Returns HttpResponseBadRequest if no ID is specifed in the GET data, HttpResponse(404) if there is no
        comment with the given ID, otherwise returns HttpResponse(200) with the JSON encoded comment.
        """
        if 'id' not in request.GET:
            return HttpResponseBadRequest("No id given")
        try:
            comment = models.Comment.objects.get(id=request.GET['id'])
        except models.Comment.DoesNotExist:
            return HttpResponse('Comment not found', status=404)
        return HttpResponse(comment.to_json(), status=200, content_type='application/json')

    @auth_required
    def post(self, request):
        """
        Creates a new comment with the given request's POST data.
        :param request: HTTP POST Request
        :return: Returns HttpResponseBadRequest if the POST data is missing any attributes required to create a comment,
        HttpResponse(404) if the deal specifed in the POST data doesn't exist, otherwise returns HttpResponse(200)
        """
        for required in models.Comment.REQUIRED:
            if required not in request.POST:
                return HttpResponseBadRequest(required + " not specified")

        if not models.Deal.objects.filter(id=request.POST['deal_id']).exists():
            return HttpResponse("Deal not found", status=404)

        comment = models.Comment(deal_id=models.Deal.objects.get(id=request.POST['deal_id']),
                                 user_id=request.user, creation_date=pytz.utc.localize(datetime.datetime.now()),
                                 content=request.POST['content'])
        comment.save()
        return HttpResponse(status=200)

    @auth_required
    def delete(self, request, id):
        """
        Deletes the comment with the given ID.
        :param request: HTTP DELETE Request
        :param id: ID of comment to be deleted
        :return: Returns HttpResponse(404) if there is no comment with the given ID, HttpResponseForbidden if the
        user logged in in the request is not the author of the comment and the currently logged in user is not a
        superuser, otherwise returns HttpResponse(200)
        """
        try:
            comment = models.Comment.objects.get(id=id)
        except models.Comment.DoesNotExist:
            return HttpResponse('Comment not found', status=404)

        if request.user.username != comment.user_id.username and not request.user.is_superuser:
            return HttpResponseForbidden('Only admins can do that')

        comment.delete()
        return HttpResponse(status=200)


class UserView(Resource):
    """View for handling user creation, modification, JSON and profiles"""

    def get(self, request, username=None):
        """
        If username if valid, get the corresponding user's profile page. Otherwise, extract the username from the
        request's GET data and return the corresponding user's information as JSON.
        :param request: HTTP GET Request
        :param username: Username of user who's profile is required
        :return: If username is given, returns HttpResponse(404) if there is no user with said username, or the
        corresponding user's profile page. If the username if not given, returns HttpResponseBadRequest if there is no
        username in the request's GET data, HttpResponse(404) if there is no user with the username in the GET data,
        otherwise returns HttpResponse(200) with the corresponding user's details as JSON.
        """
        if username:
            try:
                user = models.User.objects.get(username=username)
            except models.User.DoesNotExist:
                return HttpResponse('User does not exist', status=404)
            context = {
                'user': user,
                'deals': models.Deal.objects.filter(user_id=user)
            }
            return render(request, 'dondapp/profile.html', context=context)
        else:
            if 'username' not in request.GET:
                return HttpResponseBadRequest('No username given')

            if not models.User.objects.filter(username=request.GET['username']).exists():
                return HttpResponse('User not found', status=404)

            user = models.User.objects.get(username=request.GET['username'])
            return HttpResponse(user.to_json(), status=200, content_type='application/json')

    def post(self, request):
        """
        If the username in the given POST request's data is known, modify the corresponding user's details based on the
        POST data, otherwise create a new user with the POST data.
        :param request: HTTP POST Request
        :return: If no user name is in the POST data, returns HttpResponseBadRequest. If the given username already
        exits, returns HttpResponse(401) if the user is not logged in, HttpRequestForbidden if the current user is not
        the user to be modified and is not a superuser, if password is specifed in the POST data the user will be logged
        out, otherwise redirect to the home page. If the username doesn't already exist, returns HttpResponseBadRequest
        if any attribute required to create a user is missing or the username is taken, otherwise logs the new user in.
        """
        if 'username' in request.POST:
            if models.User.objects.filter(username=request.POST['username']).exists():
                if not request.user.is_authenticated:
                    return HttpResponse(status=401)

                if request.user.username != request.POST['username'] and not request.user.is_superuser:
                    return HttpResponseForbidden('Only admins can do that')

                # Update existing user
                user = models.User.objects.get(username=request.POST['username'])
                for attr in models.User.UPDATEABLE:
                    if attr in request.POST:
                        setattr(user, attr, request.POST[attr])

                # Only let superuser's change authority
                user.authority = request.POST.get('authority', user.authority) if user.is_superuser else user.authority
                user.save()

                if 'password' in request.POST:
                    return LoginView.delete(request)
                else:
                    return redirect('home')
            else:
                # Create new user
                for required in models.User.REQUIRED:
                    if required not in request.POST:
                        return HttpResponseBadRequest(required + " not specified")

                user = models.User.objects.create_user(request.POST['username'], request.POST['first_name'],
                                                       request.POST['last_name'], request.POST['email'],
                                                       request.POST['password'], request.POST.get('likes', default=0),
                                                       authority=False)
                user.save()
                # Log the user in after they register
                return LoginView().post(request)
        else:
            return HttpResponseBadRequest("No username specified")


class LoginView(Resource):
    """View for handling login requests"""

    def post(self, request):
        """
        Using the username and password from the given request's POST data, logs the corresponding user in.
        :param request: HTTP POST Request
        :return: Returns HttpResponseBadRequest if the POST data doesn't contain either a username or password. If the
        credentials successfully login, returns a redirect to the home page, otherwise returns a redirect to the failed
        page
        """
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
        """Logout the user in the given given request"""
        logout(request)
        return HttpResponse(status=200)


class VoteView(Resource):
    """View for handling voting"""

    @auth_required
    def post(self, request):
        """
        Adds an upvote or downvote to the deal in the request
        :param request: HTTP POST request
        :return: Returns HttpReponseBadRequest if either no deal or vote is specified, HttpResponse(404) if the deal
        does not exists returns HttpResponse with HTTP OK status if the deal's votes are successfully modified
        """

        data = json.loads(request.body)
        if 'deal_id' not in data:
            return HttpResponseBadRequest('Deal ID not specified')
        if 'upvote' not in data:
            return HttpResponseBadRequest('Upvote not specified')
        try:
            deal = models.Deal.objects.get(id=data['deal_id'])
        except models.Deal.DoesNotExist:
            return HttpResponse('Deal not found', status=404)
        if data['upvote']:
            deal.upvotes += 1
            deal.upvoters.add(request.user)
        else:
            deal.downvotes += 1
            deal.downvoters.add(request.user)

        deal.save()
        return HttpResponse(status=200)

    def get(self, request):
        """
        Returns the upvote and downvote values of the deal specified in the given request
        :param request: HTTP Get request
        :return: Returns HttpResponseBadRequest if no deal is specified, HttpResponse(404) if the deal is not found or
        HttpResponse with HTTP OK status and the following JSON body:
        {
            'upvotes': upvotes as int,
            'downvotes': downvotes as int
        }
        """

        if "deal_id" not in request.GET:
            return HttpResponseBadRequest("No deal specified")
        deal_id = request.GET["deal_id"]
        try:
            deal = models.Deal.objects.get(id=deal_id)
        except models.Deal.DoesNotExist:
            return HttpResponse('Deal not found', status=404)
        response_data = {
            'upvotes': deal.upvotes,
            'downvotes': deal.downvotes,
            'upvoters': list(deal.downvoters.values_list('username', flat=True)[:]),
            'downvoters': list(deal.downvoters.values_list('username', flat=True)[:]),
        }
        return HttpResponse(json.dumps(response_data), status=200, content_type='application/json')
