from sanic.request import Request
from sanic.response import redirect

from .manager import AuthManager
from .configuration import AuthConfig
from app.utils.configuration import config

from app.server import logger

auth_config = AuthConfig(config)


def auth(
    requires_all=None,
    requires_one_of=None,
    redirect_to=None,
    authoriser=AuthManager,
    auth_config=auth_config,
):
    """
    Authorization decorator

    requires_all: a list of roles, a use must have ALL the roles to access the decorated resource
    requeres_one_of: a list of roles, a use must have ONE (or more) of the roles to access the decorated
    resource.
    redirect_to: a uri the user will be redirected to if not authorised.
    authoriser: specify the the authorising class being used, for testing purposes.
    auth_config: specify the auth configuration used, for testing purposes.
    """

    def decorator(function):
        def wrapper(*args, **kwargs):

            # Police passing in Sanic.request where expected
            # Note - this will never fail at runtime
            # (unless we push broken code)
            assert isinstance(args[0], Request)
            request = args[0]
            auth = authoriser(auth_config, request, logger)

            # "requires_all" scenario
            if requires_all:
                allowed = True
                for role in requires_all:
                    if not auth._has_role(role):
                        allowed = False

            # "requires_one_of" scenario
            elif requires_one_of:
                allowed = False
                for role in requires_one_of:
                    if auth._has_role(role):
                        allowed = True

            else:
                # Roles not provided:
                # Pass through the auth class to allow
                # granular control within the endpoint handler
                return function(auth, *args, **kwargs)

            # Where roles were provided, this response will
            # either be allowed or not

            if not allowed:
                if redirect_to:
                    return redirect(redirect_to)
                else:
                    return redirect("/")
            else:
                return function(*args, **kwargs)

        return wrapper

    return decorator
