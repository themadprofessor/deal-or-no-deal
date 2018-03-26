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
    if request.user.is_authenticated:
        context = kwargs.get('context', {})
        if 'categories' not in context:
            context['categories'] = models.Category.objects.all()
            kwargs['context'] = context
    return django_render(request, *args, **kwargs)


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


class SearchView(Resource):
    def get(self, request):
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
    def get(self, request, id=None):
        try:
            deal = models.Deal.objects.get(id=id)
        except models.Deal.DoesNotExist:
            return HttpResponse('Deal not found', status=404)
        context = {
            'deal': deal,
            'comments': models.Comment.objects.filter(deal_id=id),
            'upvoters': deal.upvoters.values_list('username', flat=True),
            'downvoters': deal.downvoters.values_list('username', flat=True)
        }
        return render(request, 'dondapp/deal.html', context=context)

    def post(self, request):
        print(request.POST)
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
    def get(self, request):
        deals = models.Deal.objects.all()
        data = []
        for deal in deals:
            data.append(deal.to_dict())
        data = sorted(data, key=lambda x:x["creation_date"])
        return HttpResponse(json.dumps(data), status=200, content_type="application/json")
        
        
class TopDealView(Resource):
    def get(self, request):
        deals = models.Deal.objects.all()
        data = []
        for deal in deals:
            data.append(deal.to_dict())
        data = sorted(data, key=lambda x:x["upvotes"],reverse=True)
        return HttpResponse(json.dumps(data), status=200, content_type="application/json")


class CommentView(Resource):
    def get(self, request):
        if 'id' not in request.GET:
            return HttpResponseBadRequest("No id given")
        comment = models.Comment.objects.get(id=request.GET['id'])
        return HttpResponse(comment.to_json(), status=200, content_type='application/json')

    @auth_required
    def post(self, request):
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
        try:
            comment = models.Comment.objects.get(id=id)
        except models.Comment.DoesNotExist:
            return HttpResponse('Comment not found', status=404)

        if request.user.username != comment.user_id.username and not request.user.is_superuser:
            return HttpResponseForbidden('Only admins can do that')

        comment.delete()
        return HttpResponse(status=200)


class UserView(Resource):
    def get(self, request, username=None):
        if username:
            user = models.User.objects.get(username=username)
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
            return HttpResponse(user.to_json(), status=200)

    def post(self, request):
        if 'username' in request.POST:
            if models.User.objects.filter(username=request.POST['username']).exists():
                if not request.user.is_authenticated:
                    return HttpResponse(status=401)

                if request.user.username != request.POST['username'] and not request.user.is_superuser:
                    return HttpResponseForbidden('Only admins can do that')

                # Update existing user
                user = models.User.objects.get(username=request.POST['username'])
                for attr in models.User.UPDATEABLE:
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

                if models.User.objects.filter(username=request.POST['username']).exists():
                    return HttpResponseBadRequest("Username is taken")

                user = models.User.objects.create_user(request.POST['username'], request.POST['first_name'],
                                                       request.POST['last_name'], request.POST['email'],
                                                       request.POST['password'], request.POST.get('likes', default=0),
                                                       authority=False)
                user.save()
                # Log the user in after they register
                return LoginView().post(request)


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
