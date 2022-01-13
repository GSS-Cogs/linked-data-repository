from sanic import Sanic
from sanic.request import Request
from sanic.response import redirect, json
from sanic.log import logger

from utils import get_config, AuthConfig
from auth import Auth

app = Sanic(name="backend")

app.ctx.cfg = get_config(logger)

ac = AuthConfig(app.ctx.cfg)

def respond_update_cookie(request: Request, response, cookie: str):
    """
    Do the right things when writing a user cookie
    along with a response.
    """
    response.cookies["user"] = cookie
    response.cookies['user']['httponly'] = True
    response.cookies['user']['secure'] = True
    
    # Note - split as it needs to be "localhost" not "localhost:<port>"
    # TODO - use a library to make url, not nasty splits
    response.cookies['user']['domain'] = f'{request.host.split(":")[0]}'

    return response


@app.route('/')
async def home(request: Request):
    """
    Super simple endpoint, returns some json
    """
    auth = Auth(ac, request, logger)
    return json({"you're logged in as an admin": auth.has_admin()}, status=200)


@app.route('/login')
async def login(request: Request):
    """
    Sends a user to log in and authenticate via the provider
    (google via auth0). If successful, auth0 will redirect back
    to /callback
    """
    auth = Auth(ac, request, logger)
    uri = auth.get_auth_uri()
    return respond_update_cookie(
        request,
        redirect(uri),
        auth.cookie
    )


@app.route('/callback')
async def callback_handling(request: Request):
    """
    Receives redirected request from auth0 once a user
    has been authenticated. Then encrypts access
    token into the user cookie and redirects
    us back to /.
    """
    auth = Auth(ac, request, logger)
    auth.set_access_token()
    return respond_update_cookie(
        request,
        redirect('/'),
        auth.cookie
    )


@app.route('/logout')
async def logout(request: Request):
    """
    Logs the user out, both on auth0 and via removing the
    users access token from their user cookie.
    """
    auth = Auth(ac, request, logger)
    auth.logout()
    return respond_update_cookie(
        request,
        redirect('/'),
        auth.cookie
    )


if __name__ == "__main__":
    # note: for development, i.e when you `pipenv run python3 ./app/server.py`
    app.run(host="localhost", port=3000, debug=True, access_log=True)