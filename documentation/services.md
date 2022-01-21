
## Services

We've implemented a simple composable drivers pattern for this service, revolving around using `create_app` from `app/server.py`.

The allows:

* Easy use of stubs and/or changing of drivers during development.
* Easy implemented composable tests.

Drivers can be specified to `create_app` as:
* Instantiated objects (for example, when creating test mocks)
* A string label mapping to a defined driver.

_Note: The functionality for supporting selecting drivers by label is to allow for specifiying driver via configuration rather than application code._

### Adding a new service driver

All modular service drivers used by this app are created in the same way:

* Create relevant base class as `app/services/<name of new service>/base.py`
* Implement at least one driver in `app/services/<name of new service>/drivers/<name of driver>.py`
* Create a text to driver mapping dict in `app/services/inventory.py`
* Create a "get service" wrapper in `app/services/composer.py`
* Add your new service driver to the `create_app` constructor in `app/server.py` 


### Testing

The easiest way to do this is to instantiate a `unittest.mock.Mock()` class with appropriate methods and pass it in place of an instantiated driver.

```python

from app.server import create_app
from unittest.mock import Mock

def test_for_getting_a_record():
    """
    Hyperthetical test where our app needs to get a record from the "Store"
    to test some other piece of fuctionality.
    """
    test_store = Mock()
    test_store.get_record = lambda: {"mock": "record"}

    app = create_app(
        store=test_store,
        sanic_test_mode = True,
        enforce_base_classes = False
        )

    # do your test

```

Keywords in the above example:

* `sanic_test_mode` - disables Sanic automated caching of every instantiated app (this can lead to namespace clashes while testing).  
* `enforce_base_classes` - toggles off the driver type check, otherwise an exception would be raised as `mock.Mock` does not extend `BaseStore`.