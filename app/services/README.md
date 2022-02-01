
## Services

When you `create_app`, the implementation you wish to be injected will be specified in one of following ways:

* Classes will be directly passed in (mainly for testing, i.e `Mock()`, see example).
* A str that maps to a known implementation via `app.services.inventory.INVENTORY`
* None (don't specify). This will tell the app to take the str choice as defined in configuration.ini.
* You can also pass a `configparser.ConfigParser` instance directly to the `create_app` constructor should you need to (again, this is mainly for tests).

The principle benefit is to retain flexibility to work with an MVP "good enough for now" or develoment only services, easily swapping to production ready (or generally better) services as and when we need/want to.


### Adding a new service

Service interfaces are secured using the python `Protocol` class, you can add new ones with the following steps.

* Create relevant interface in `app/interfaces`.
* Create implementation(s) inside the `services` module - this _should_ always include a `Nop` (non operational) handler - see `app/services/store/nop.py` for an example.
* Inject an alias to the appropriate interface for each new handler, this enables runtime type checking, the decorator pattern will look something like `@inject(alias=interfaces.MyNewInterface)`.
* Create an entry for your new service in the configuration.
* Define how your handler(s) use this configuration in `app/services/container`.
* Add your new app to the constrcutors for `create_app` and `_bootstrap_app` in `app/server.py`.
* Expand tests to cover newly implemented functionality.


### Testing


```python

from app.server import create_app
from app.service.store import NopStore

def test_for_getting_a_record():
    """
    Hyperthetical test where our app needs to get a record from the "Store"
    to test some other piece of fuctionality.
    """
    test_store = Mock
    test_store.get_record = MethodType(lambda x: {"mock": "record"}, test_store)

    app = create_app(store=test_store, messenger='Nop', sanic_test_mode=True)

    assert app.ctx.store.get_record() == {"mock": "record"}

    # do your test

```

In the above example, the kwarg `sanic_test_mode = True` disables Sanic automated caching of every instantiated app (this can lead to namespace clashes, so is recommended for tests).  

**Please note:** If you don't pass a keyword in for a service it defaults to `None` and uses whatever is specified as the default via the apps configuration - which means a configuration change could potentially change test behaviour. Therefore while testing always either (a) explicitly specify each service handler as per the above or (b) pass in an appropriate `configparser.ConfigParser()` object (i.e include a configuration fixture in your test setup).