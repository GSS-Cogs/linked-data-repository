from sanic.response import json
from exceptions import (
    AccessDeniedError,
    ConfigurationConflictError,
    FreshTokenRequiredError,
    InvalidHeaderError,
    JWTDecodeError,
    NoAuthorizationError,
    RevokedTokenError,
    WrongTokenError,
)


class Handler:
    default_message_key = "msg"

    no_authorization = staticmethod(
        lambda r, e: json({Handler.default_message_key: str(e)}, 401)
    )
    expired_signature = staticmethod(
        lambda r, e: json({Handler.default_message_key: str(e)}, 401)
    )
    invalid_header = staticmethod(
        lambda r, e: json({Handler.default_message_key: str(e)}, 422)
    )
    invalid_token = staticmethod(
        lambda r, e: json({Handler.default_message_key: str(e)}, 422)
    )
    jwt_decode_error = staticmethod(
        lambda r, e: json({Handler.default_message_key: str(e)}, 422)
    )
    wrong_token = staticmethod(
        lambda r, e: json({Handler.default_message_key: str(e)}, 422)
    )
    revoked_token = staticmethod(
        lambda r, e: json({Handler.default_message_key: str(e)}, 401)
    )
    fresh_token_required = staticmethod(
        lambda r, e: json({Handler.default_message_key: str(e)}, 401)
    )
    access_denied = staticmethod(
        lambda r, e: json({Handler.default_message_key: str(e)}, 403)
    )

    @classmethod
    def _set_error_handlers(cls, app):
        app.error_handler.add(
            NoAuthorizationError,
            cls.handler.no_authorization)
        app.error_handler.add(
            ExpiredSignatureError,
            cls.handler.expired_signature)
        app.error_handler.add(InvalidHeaderError, cls.handler.invalid_header)
        app.error_handler.add(InvalidTokenError, cls.handler.invalid_token)
        app.error_handler.add(JWTDecodeError, cls.handler.jwt_decode_error)
        app.error_handler.add(WrongTokenError, cls.handler.wrong_token)
        app.error_handler.add(RevokedTokenError, cls.handler.revoked_token)
        app.error_handler.add(
            FreshTokenRequiredError,
            cls.handler.fresh_token_required)
        app.error_handler.add(AccessDeniedError, cls.handler.access_denied)
