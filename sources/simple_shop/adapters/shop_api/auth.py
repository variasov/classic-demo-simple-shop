from functools import wraps


# Stub for demo purposes. Real auth will be published later
def auth(function):

    @wraps(function)
    def wrapper(controller, request, response, *args):
        request.context.client_id = 1
        return function(controller, request, response, *args)

    return wrapper
