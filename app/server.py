from sanic import Sanic
from sanic.request import Request
from sanic.response import redirect, json
from sanic.log import logger

from utils import get_config, SessionConfig
from session import Session

app = Sanic(name="backend")

app.ctx.cfg = get_config(logger)

sc = SessionConfig(app.ctx.cfg)

def respond_update_session(request: Request, response, cookie: str):
    """
    Do the right things when writing a session cookie
    along with a response.
    """
    response.cookies["session"] = cookie
    response.cookies['session']['httponly'] = True
    response.cookies['session']['secure'] = True
    
    # Note - split as it needs to be "localhost" not "localhost:<port>"
    # TODO - use a library to make url, not nasty splits
    response.cookies['session']['domain'] = f'{request.host.split(":")[0]}'

    return response


@app.route('/')
async def home(request: Request):
    """
    Super simple endpoint, returns some json
    """
    session = Session(sc, request, logger)
    return json({"you're logged in as an admin": session.has_admin()}, status=200)


@app.route('/login')
async def login(request: Request):
    """
    Sends a user to log in and authenticate via the provider
    (google via auth0). If successful, auth0 will redirect back
    to /callback
    """
    session = Session(sc, request, logger)
    uri = session.get_auth_uri()
    return respond_update_session(
        request,
        redirect(uri),
        session.cookie
    )


@app.route('/callback')
async def callback_handling(request: Request):
    """
    Receives redirected request from auth0 once a user
    has been authenticated. Then encrypts access
    token into the session cookie and redirects
    us back to /.
    """
    session = Session(sc, request, logger)
    session.set_access_token()
    return respond_update_session(
        request,
        redirect('/'),
        session.cookie
    )


@app.route('/logout')
async def logout(request: Request):
    """
    Logs the user out, both on auth0 and via removing the
    users access token from their session cookie.
    """
    session = Session(sc, request, logger)
    session.logout()
    logger.debug(session.decode_session_cookie())
    return respond_update_session(
        request,
        redirect('/'),
        session.cookie
    )


if __name__ == "__main__":
    # note: for development, i.e when you `pipenv run python3 ./app/server.py`
    app.run(host="localhost", port=3000, debug=True, access_log=True)