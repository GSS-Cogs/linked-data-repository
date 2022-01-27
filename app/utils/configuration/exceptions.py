class JWTExtendedException(Exception):
    """
    Base except which all sanic_jwt_extended errors extend
    """

    ...


class JWTDecodeError(Exception):
    """
    An error decoding a JWT
    """

    ...


class InvalidHeaderError(Exception):
    """
    An error getting header information from a request
    """

    ...


class NoAuthorizationError(Exception):
    """
    An error raised when no authorization token was found in a protected endpoint
    """

    ...


class WrongTokenError(Exception):
    """
    Error raised when attempting to use a refresh token to access an endpoint
    or vice versa
    """

    ...


class RevokedTokenError(Exception):
    """
    Error raised when a revoked token attempt to access a protected endpoint
    """

    ...


class FreshTokenRequiredError(Exception):
    """
    Error raised when a valid, non-fresh JWT attempt to access an endpoint
    protected by jwt_required with fresh_required is True
    """

    ...


class AccessDeniedError(Exception):
    """
    Error raised when a valid JWT attempt to access an endpoint
    protected by jwt_required with not allowed role
    """


class CSRFError(Exception):
    ...
