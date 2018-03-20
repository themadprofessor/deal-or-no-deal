from django.http import Http404, HttpResponseNotAllowed, HttpResponse, HttpResponseForbidden


def get_handler_method(request_handler, http_method):
    try:
        handler_method = getattr(request_handler, http_method.lower())
        if callable(handler_method):
            return handler_method
    except AttributeError:
        pass


class Resource:

    http_methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS', 'TRACE']

    @classmethod
    def dispatch(cls, request, *args, **kwargs):
        request_handler = cls()

        if request.method in cls.http_methods:
            handler_method = get_handler_method(request_handler, request.method)
            if handler_method:
                return handler_method(request, *args, **kwargs)

        methods = [method for method in cls.http_methods if get_handler_method(request_handler, method)]
        if len(methods) > 0:
            return HttpResponseNotAllowed(methods)
        else:
            raise Http404


def auth_required(func):
    def wrapper(request, *args, **kw):
        user = args[0].user
        if not user.is_authenticated:
            return HttpResponse("Not logged in", status=401)
        else:
            return func(request, *args, **kw)
    return wrapper


def authority_required(func):
    @auth_required
    def wrapper(request, *args, **kwargs):
        user = args[0].user
        if user.authority:
            return func(request, *args, *kwargs)
        else:
            return HttpResponseForbidden("Only admins can do that!")
    return wrapper
