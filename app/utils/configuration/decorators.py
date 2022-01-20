from functools import wraps


def authorised(func):
    def authoriser(name=None):
        @wraps(func)
        async def decorated_function(request, *args, **kwargs):
            # if 'upload' in request.url: TO DO: mapping to permission/role
            # system
            response = f(request, *args, **kwargs)
            if isawaitable(response):
                response = await response

            return response
        return decorated_function
    return authoriser
