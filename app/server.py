from sanic import Sanic
from sanic.request import Request
from sanic.response import redirect, text
from sanic.log import logger

from app.utils.auth import AuthManager, auth
from app.utils.cookies import respond_update_cookie
from app.utils.configuration import config

app = Sanic(name="backend")
app.ctx.cfg = config

@app.route('/')
async def home(request: Request):
    return text("home endpoint that doesn't really do anything")


# EXAMPLE - remove
@app.route("/allowed")
@auth(requires_all=["admin"], redirect_to="/not-allowed")
async def allowed(request: Request):
    """
    Example of simple auth wrapped endpoint.
    Redirects to '/not-allowed' if they don't have
    an "admin" role.
    """
    return text("someone has auth!")


# EXAMPLE - remove
@app.route("/not-allowed")
async def not_allowed(request: Request):
    """
    Super simple text response for a no auth person
    """
    return text("someone got redirected after not having auth!")


# EXAMPLE - remove
@app.route("/might-be-allowed")
@auth()
async def not_allowed(auth: AuthManager, request: Request):
    """
    Example of an endpoint where the response varies based on the role
    of the calling user
    """

    if auth._has_role("admin"):
        return text(
            'I\'m the version of the "maybe-auth" endpoint for people with the "admin" role!'
        )
    else:
        return text(
            'I\'m the version of the "maybe-auth" endpoint for people without the "admin" role!'
        )


@app.route("/login")
@auth()
async def login(auth: AuthManager, request: Request):
    """
    Sends a user to log in and authenticate via the provider
    (google via auth0). If successful, auth0 will redirect back
    to /callback
    """
    uri = auth.get_auth_uri()
    return respond_update_cookie(request, redirect(uri), auth.cookie)


@app.route("/callback")
@auth()
async def callback_handling(auth: AuthManager, request: Request):
    """
    Receives redirected request from auth0 once a user
    has been authenticated. Then encrypts access
    token into the user cookie and redirects
    us back to /.
    """
    auth.set_access_token()
    return respond_update_cookie(request, redirect("/"), auth.cookie)


@app.route("/logout")
@auth()
async def logout(auth: AuthManager, request: Request):
    """
    Logs the user out, both on auth0 and via removing the
    users access token from their user cookie.
    """
    auth.logout()
    return respond_update_cookie(request, redirect("/"), auth.cookie)
