from configparser import ConfigParser

# TODO - seemed like a good idea but is a little messier that I'd envisoned
# try it in anger for a bit but don't be afraid to refactor.
class SessionConfig:
    """
    Convenience for neater session releveant variables taken or
    extrapolated from the wider app config
    """

    def __init__(self, cfg: ConfigParser):
        oauth_domain = cfg.get('ENV', 'oauth_domain')

        # Auth related standard config
        self.session_expiry_minutes = int(cfg.get('AUTH', 'session_timeout_minutes'))
        self.algorithm = cfg.get('AUTH', 'jwt_encoding_algorithm')
        self.roles_namespace = cfg.get('AUTH', 'roles_namespace')

        # Things that started as env vars
        self.encryption_key = cfg.get('ENV', 'session_encryption_key')
        self.client_id = cfg.get('ENV', 'oauth_client_id')
        self.client_secret = cfg.get('ENV', 'oauth_client_secret')
        self.redirect_uri = cfg.get('ENV', 'oauth_redirect_uri')

        # Extrapolated
        self.access_token_url = f'https://{oauth_domain}/oauth/token'
        self.authorize_url = f'https://{oauth_domain}/authorize'
        self.userinfo_url = f'https://{oauth_domain}/userinfo'
        self.logout_url = f'https://{oauth_domain}/v2/logout'