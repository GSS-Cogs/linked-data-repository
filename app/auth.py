import datetime
import jwt

from authlib.integrations.requests_client import OAuth2Session
# TODO - is there a built-in sanic.request GET handler? seems likely
import requests
from sanic.request import Request

from app.utils import AuthConfig


class Auth:
    """
    A thing to handle the encryption and decryption of an auth related cookie,
    also holds associated authentication and authorization methods.
    """

    def __init__(self, cfg: AuthConfig, request: Request, logger):
        self.cfg = cfg
        self.logger = logger
        self.request = request
   
        self.client = OAuth2Session(
            self.cfg.get('client_id', None),
            self.cfg.get('client_secret', None),
            scope='openid',
            redirect_uri=self.cfg.get('redirect_uri', None)
        )

        self.cookie = request.cookies.get('user', None)
        if not self.cookie:
            self.pristine()

    def encrypt_cookie(self, sub_dict):
        """
        Encrypts the self.cookie with the provided sub_dict as
        the "sub" field.
        """

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=0,
                    hours=0,
                    minutes=self.cfg.get('expiry_minutes', None)
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': sub_dict
            }
            self.cookie = jwt.encode(
                payload,
                self.cfg.get('encryption_key', None),
                algorithm=self.cfg.get('algorithm', None)
            )
        except Exception as err:
            self.logger.error(
                f'Failed to encrypt cookie with exception:\n {err}'
                '\n Payload was {payload}')
            raise err

    def decrypt_cookie(self, time_stamps: bool = False) -> (dict):
        """
        Decrypt the cookie, of structure:

        {
            "sub":
        }

        If time_stamps = True we return whole cookie, otherwiswe just ["sub"]
        """
        try:
            payload = jwt.decode(
                self.cookie,
                self.cfg.encryption_key,
                algorithms=self.cfg.algorithm)
            if not time_stamps:
                payload = payload.get('sub', None)
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
        Set a single field in the .cookie["sub"] dict
        """
        sub_dict = self.decrypt_cookie()
        sub_dict[key] = value
        self.encrypt_cookie(sub_dict)

    def get(self, key):
        """
        Get a single field from the .cookie["sub"] dict
        """
        try:
            sub_dict = self.decrypt_cookie()
            return sub_dict.get(key, None)
        except KeyError:
            self.logger.warning(
                f'Unable to find key "{key}" in cookie. Got {sub_dict.keys()}')
            return None

    def remove(self, key):
        """
        Delete a single field from the .cookie["sub"] dict
        """
        sub_dict = self.decrypt_cookie()
        if not sub_dict.pop(key, None):
            self.logger.warning(
                f'Called Auth.remove() for field "{key}" but no '
                'such field existed in the ["sub"] dict')
        self.encrypt_cookie(sub_dict)

    def get_auth_uri(self):
        """
        Get the authentication url, also sets state against .cookie["sub"]["state"]
        """
        uri, state = self.client.create_authorization_url(
            self.cfg.authorize_url)
        self.set("state", state)
        return uri

    def get_access_token(self):
        """
        Gets access_token
        """
        token_dict = self.get_token()
        return token_dict["access_token"]

    def set_access_token(self):
        """
        Gets and then sets an access_token against .cookie["sub"]["access_token"]
        """
        access_token = self.get_access_token()
        self.set("access_token", access_token)

    # TODO - we might be able to use some of the "id_token" information for security,
    # for example: check intended recipient, I _think_ it should match
    # self.cfg.client_id)

    def get_token(self) -> (dict):
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
        the cookie.
        """

        r = requests.get(
            self.cfg.logout_url, headers={
                "client_id": self.cfg.client_id})
        if r.status_code != 200:
            self.logger.warning(
                f'Logout failed at {self.cfg.logout_url} with status code {r.status_code}')
        else:
            self.remove("access_token")

    # TODO - in production this should be more generic, look for _something_
    # in _some_ namespace. The equivient of _has_role() should just wrap that.

    def _has_role(self, role) -> (bool):
        """
        Given the access token from the cookie, does the user in question have
        the queried role under the self.cfg.roles_namespace key.
        """

        # Treat no token as does not have role, we don't want to be directing
        # public users through a login.
        decoded_cookie = self.decrypt_cookie()
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
        Does the current user cookie contain an access token that
        identifies them as having then "admin" role under the
        roles_namespace key.
        """
        return self._has_role("admin")

    def pristine(self):
        """
        Resets to a pristine (empty other than time stamps) cookie
        """
        self.encrypt_cookie({})
