import datetime
import jwt

from authlib.integrations.requests_client import OAuth2Session
# TODO - is there a built-in sanic.request GET handler? seems likely
import requests
from sanic.request import Request

from utils import SessionConfig

# Since we're always calling this on many endpoints, it's probably a decorator longer term.
# I'm also not sure it's "Session", it might be "Auth" that just so happens to encrypt/decrypt
# a session cookie.
class Session:
    """
    A thing to handle the encryption and decryption of browser session tokens,
    also holds associated auth methods.
    """
    
    def __init__(self, cfg: SessionConfig, request: Request, logger):
        self.cfg = cfg
        self.logger = logger
        self.request = request

        self.client = OAuth2Session(
            self.cfg.client_id,
            self.cfg.client_secret,
            scope='openid',
            redirect_uri=self.cfg.redirect_uri
        )

        self.cookie = request.cookies.get('session', None)
        if not self.cookie:
            self.pristine()

    # TODO: encrypt not encode
    def encode_session_cookie(self, sub_dict):
        """
        Sets the session cookie with the provided sub_dict as
        the "sub" field.
        """

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=0,
                    hours=0,
                    minutes=self.cfg.session_expiry_minutes
                    ),
                'iat': datetime.datetime.utcnow(),
                'sub': sub_dict
            }
            self.cookie = jwt.encode(
                payload,
                self.cfg.encryption_key,
                algorithm=self.cfg.algorithm
            )
        except Exception as err:
            self.logger.error(f'Failed to encode session cookie with exception:\n {err}'
                '\n Payload was {payload}')
            raise err


    # TODO: decrypt not decode
    def decode_session_cookie(self, time_stamps=False) -> (dict):
        """
        Decodes the session cookie
        """
        try:
            payload = jwt.decode(self.cookie, self.cfg.encryption_key, algorithms=self.cfg.algorithm)
            if not time_stamps:
                payload = payload['sub']
            return payload

        except jwt.ExpiredSignatureError as err:
            self.logger.error(err)
            # TODO - handle this properly
            raise err

        except Exception as err:
            # TODO - handle this properly
            raise err


    def set(self, key, value):
        """
        Set a single field in the session ["sub"] dict
        """
        sub_dict = self.decode_session_cookie()
        sub_dict[key] = value
        self.encode_session_cookie(sub_dict)


    def get(self, key):
        """
        Get a single field from the session ["sub"] dict
        """
        try:
            sub_dict = self.decode_session_cookie()
            return sub_dict.get(key, None)
        except KeyError:
            self.logger.warning(f'Unable to find key "{key}" in session cookie. Got {sub_dict.keys()}')
            return None


    def remove(self, key):
        """
        Delete a single field from the session ["sub"] dict
        """
        sub_dict = self.decode_session_cookie()
        if not sub_dict.pop(key, None):
            self.logger.warning(f'Called Session.remove() for field "{key}" but no '
                'such field existed in the ["sub"] dict')
        self.encode_session_cookie(sub_dict)


    def get_auth_uri(self):
        uri, state = self.client.create_authorization_url(self.cfg.authorize_url)
        self.set("state", state)
        return uri


    def get_access_token(self):
        token_dict = self.get_token()
        return token_dict["access_token"]


    def set_access_token(self):
        access_token = self.get_access_token()
        self.set("access_token", access_token)


    def get_token(self):
        """
        Gets the token(s) response from auth0, example:
        
        {   
            'access_token': <str>
            'id_token': <str>,
            'scope': 'openid',
            'expires_in': <int>.
            'token_type': 'Bearer',
            'expires_at': <int>
        }
        """

        state = self.request.args.get("state", None)
        if not state:
            # TODO - handle this properly
            raise Exception('Callback url should contain a "state" param')
      
        # Confirm auth server returned state matches initial
        # state (guard against CSRF attacks)
        # TODO - what do we do if it doesen't?        
        assert state == self.get("state")

        # Don't linger state once it's served its purpose
        self.remove("state")

        return self.client.fetch_token(
            self.cfg.access_token_url,
            authorization_response=self.request.url)


    def logout(self):
        """
        Logs the user out via auth0 api.
        
        If that is successful, also removes the users token from
        the session cookie.
        """

        r = requests.get(self.cfg.logout_url, headers = {"client_id": self.cfg.client_id})
        if r.status_code != 200:
            self.logger.warning(f'Logout failed at {self.cfg.logout_url} with status code {r.status_code}')
        else:
            self.remove("access_token")


    def _has_role(self, role) -> (bool):
        """
        Given the access token from the session, does the user in question have
        the queried role under the self.cfg.roles_namespace key.
        """

        # Treat no token as does not have role, we don't want to be directing
        # public users through a login.
        decoded_cookie = self.decode_session_cookie()
        if 'access_token' not in decoded_cookie:
            return False

        # Use token to get user information
        headers = {'Authorization': f'Bearer {decoded_cookie["access_token"]}'}
        r = requests.post(self.cfg.userinfo_url, headers=headers)
        if not r.ok:
            # TODO - handle this properly
            raise NotImplementedError('Logout url not working')
        self.logger.debug(f'Logout got status code {r.status_code}')
        
        user_info = r.json()

        # User has authenticated, but has no assigned roles
        if self.cfg.roles_namespace not in user_info:
            return False

        return role in user_info[self.cfg.roles_namespace]


    def has_admin(self) -> (bool):
        """
        Does the current user sessions contain an access token that
        identifies them as having then "admin" role under the
        roles_namespace key.
        """
        return self._has_role("admin")


    def pristine(self):
        """
        Resets to a pristine (empty other than time stamps) session cookie
        """
        self.encode_session_cookie({})

