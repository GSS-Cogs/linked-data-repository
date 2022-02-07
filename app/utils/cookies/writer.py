from sanic.request import Request


def respond_update_cookie(request: Request, response, cookie: str):
    """
    Do the right things when writing a user cookie
    along with a response.
    """
    response.cookies["user"] = cookie
    response.cookies["user"]["httponly"] = True
    response.cookies["user"]["secure"] = True

    # Note - split as it needs to be "localhost" not "localhost:<port>"
    # TODO - use a library to make url, not nasty splits
    response.cookies["user"]["domain"] = f'{request.host.split(":")[0]}'

    return response
