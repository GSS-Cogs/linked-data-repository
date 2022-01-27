from functools import wraps
from sanic.response import redirect
from handlers import Handler


def authorised(func):
    def authoriser(name=None):
        @wraps(func)
        async def decorated_function(request, *args, **kwargs):
            # TO DO: mapping to permission/role from user id
            response = f(request, *args, **kwargs)
            if isawaitable(response):
                response = await response
                if 'name is not authorised':
                    return redirect(
                        'base_url + error_page + message',
                        args=Handler.no_authorization)
                elif 'name is access denied':
                    return redirect(
                        'base_url + error_page + message',
                        args=Handler.access_denied)
            return response
        return decorated_function
    return authoriser
