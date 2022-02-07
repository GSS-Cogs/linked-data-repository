
## Services

When you `create_app`, the implementation you wish to be injected will be specified in one of following ways:

* Classes will be directly passed in.
* A str that maps to a known implementation via `app.services.inventory.INVENTORY`
* None (don't specify). This will tell the app to take the str choice as defined in configuration.ini.
* You can also pass a `configparser.ConfigParser` instance directly to the `create_app` constructor should you need to (this is for testing).

The principle benefit is to retain flexibility to work with an MVP "good enough for now" or develoment only services, easily swapping to production ready (or generally better) services as and when we need/want to.


### Adding a new service

Service interfaces are secured using the python `Protocol` class, you can add new ones with the following steps.

* Create relevant interface in `app/interfaces`.
* Create implementation(s) inside the `services` module - this _should_ always include a `Nop` (non operational) handler - see `app/services/store/nop.py` for an example.
* Inject an alias to the appropriate interface for each new handler, this enables runtime type checking, the decorator pattern will look something like `@inject(alias=interfaces.MyNewInterface)`.
* Create an entry for your new service in the configuration.
* Define how your handler(s) use this configuration in `app/services/container`.
* To use - decorate any handlers where your directly injected services are used with the `@inject` decorator - and pass the services as a parameter to the function (see example below). 


### Testing


```python
from kink import inject

from app.server import create_app

def test_for_getting_a_record():
    """
    Hyperthetical test where our app needs to get a record from the "Store"
    """
    test_store = NopStore
    test_store.get_record = MethodType(lambda x: {"mock": "record"}, test_store)

    @inject
    def fake_endpoint(store: interfaces.Store):
        return store.get_record()

    assert fake_endpoint() == {"mock": "record"}
```


### Other Test Considerations

Consider the following test:

```python
def test_incorrect_interface_is_raised():
    """
    The expected exception is raised if an implementation does not
    support the required protocols.
    """

    class WrongUn:
        pass

    with pytest.raises(ProtocolError):
        create_app(messenger=WrongUn, sanic_test_mode=True, config=nop_config)

```

In the above example, the kwarg `sanic_test_mode = True` disables Sanic automated caching of every instantiated app (this can lead to namespace clashes, so is recommended for tests).  

**Please note:** If you don't pass a keyword in for a service it defaults to `None` and uses whatever is specified as the default via the apps configuration - which means a configuration change could potentially change test behaviour.

Therefore while testing always either (a) explicitly specify each service implementation or (b) pass in an appropriate `configparser.ConfigParser()` object (as per the above `nop_config` kwarg value).