
## Service Composer

i.e what's in `/services` and why.

We've implemented a simple composable drivers pattern for this service, revolving around using `create_app` from `app/server.py`.

The intention is to allow us to:

* Easily use stubs and/or change drivers during development.
* Easily implement composable tests.

Drivers can be specified to the app as:
* Instantiated objects (for example, when creating test mocks)
* A string mapping to a known driver.

_Note: The rationale for supporting selecting drivers by label is to keep one eye firmly on a future goal of specifiying drivers via config rather than application code_. 

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