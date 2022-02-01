
## Services

We've implemented a simple composable pattern for interacting with dependent services (databases, message queues etc) for this app. This approach revolves around using `create_app` from [server.py](https://github.com/GSS-Cogs/linked-data-repository/tree/app/server.py) with dynamic runtime arguments.

When you `create_app` the kwargs provided will define which of the service implementations (see `app/services/<name-of-thing>/implementations/*`) are used.

The approach allows:

* Easy use of stubs and/or changing of service implementation during development.
* Easy implemented composable tests.

Services can be specified to `create_app` as:
* Instantiated objects (for example, when creating test mocks)
* A string label mapping to a implementation as defined in the [inventory](https://github.com/GSS-Cogs/linked-data-repository/tree/app/services/inventory.py) (so defaults can be specified and/or changed via config).

The principle benefit is you can start any branch of work with an MVP "good enough for now" service and easily swap in a production ready service at a later date without making any application level code changes. 

### Adding a new service

All services used by this app are created in the same way:

* Create relevant base class as `app/services/<name of new service>/base.py`
* At least one implemenation in `app/services/<name of new service>/implementations/<name>.py`
* Create a text to implementation mapping dict in `app/services/inventory.py`
* Add a constructor in `app/services/composer.py` (see `store` and `messager` for examples).
* Add your new service to the `create_app` constructor as defined in [server.py](https://github.com/GSS-Cogs/linked-data-repository/tree/app/server.py).


**IMPORTANT:** Always include a Nop (Not Operational) implementation.

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

    app = create_app(store=test_store, sanic_test_mode=True)

    assert app.ctx.store.get_record() == {"mock": "record"}

    # do your test

```

In the above example, the kwarg `sanic_test_mode = True` disables Sanic automated caching of every instantiated app (this can lead to namespace clashes, so is recommended for tests).  
