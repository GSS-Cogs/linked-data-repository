# Auth Spike

Initial spike code for OIDC auth via sanic.

**Not** productionised and no tests, proof of concept and/or/possibly a starting point.

Ive done _some_ amount of tidying up, though I suspect a blacksheep style decorator would be neater and auth as a whole may be better pulled out to its own module (would others use this? I'm thinking CMS here).

Not actually using the `id_token` for anything here, but we have access to it.

## How does this example work?

_Authenticates_ people via a google account.

_Authorises_ people based on if said google account has a `@gsscog.uk` email address, if you log in with one you're an admin, if you authenticate with any other google account - or you don't log in - you're not.

- The `/` endpoint will tell you if you're currently logged in as an admin.
- The `/login` endpoint will log you in with OIDC.
- The `/logout` endpoint will log you out.

Caching is a pig, so if you want to try different gmail accounts, its easiest to just use an incognito window.

Once logged in, your access token is stored in an encrypted cookie in the browser (http only, only sent via https, stored against this serves domain only). Until it expires or you log out, said access token is used to check your roles (i.e - do you have "admin"?) when you hit the `/` endpoint.

I have _not_ implement refresh logic or anything like that, it's just a spike.

## Setup

Set the environment variables:

| name | description |
| ---- | ----------- |
| SESSION_ENCRYPTION_KEY | When running locally a default one will be generated. |
| OAUTH_DOMAIN | Get from auth0 account/someone else. |
| OAUTH_CLIENT_ID | Get from auth0 account/someone else. |
| OAUTH_CLIENT_SECRET | Get from auth0 account/someone else. |
| OAUTH_REDIRECT_URL | When runing locally, use http://localhost:3000/callback

## Usage

```python
pipenv run ./app/server.py
```

Navigating here [http://localhost:3000/](http://localhost:3000/) to see the `/` endpoint.


## How it works

### Flow

This server is using the standard `oidc` scope. So a typical "log in with google" approach, I'm not detailed that here but it's roughly:

- this server uses its secrets (the env vars) to get an authentication url and `state` value from the auth provider (auth0).
- user is authenticated via identity provider login (google in this case)
- auth provider (auth0) redirects users response to this servers `/callback` endpoint, providing `token` and `state` values as url parameters.
- this server checks the `state` it was originally given matches the `state` parameter given to the callback url (avoid CSRF attacks, i.e confirm incoming request actually is from the auth provider).
- the `token` is permission from the user to request a scoped (to "oidc") `access_token` on their behalf - so we do.
- the `access_token` is encrypted to a `user` cookie set against this servers domain in the browser.
- the `access_token` in the cookie is used to check (per request) if a given (now `authenticated`) user has the `role` required to get the resource in question - this is `authorization`.

### Rules

Auth0 [rules](https://auth0.com/docs/customize/rules) allow you to extend the information returned from the `/userinfo` endpoint, so **after** authentication, but **before** said userinfo is returned to the app.

Im this case I've set a `rule` on an [https://auth0.com/](https://auth0.com/) account to add an `admin` permission under the roles namespace (see configuration.ini) but only for authenticated google `gsscogs.uk` users.

_Note - the roles namespace defined in the apps cofiguration **must** match the same one used in the auth `rule`._ 

In production the `rule`'s would likely be more nuanced than this (some variation of calling off to a database to get a given users roles) but the approach would/could be the same, i.e

- authenticate
- use `rule` logic to extend `userinfo` with authorisations/roles/permissions.
- `/userinfo` returned to app.
- app makes auth based decisions based on `roles` present in said userinfo.
