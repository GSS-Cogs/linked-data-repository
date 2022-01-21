
## Service Composer

i.e what's in `/services` and why.

We've implemented a simple composbale driver patterns for this service, revolving around using `create_app` from `app.server.py`.

The intention is to allow us to:

* Easily use stubs and/or change drivers during development.
* Easily implement composable tests.

Drivers can be specified to the app as:
* Instantiated objects (for example, when creating test mocks)
* A string mapping to a known driver.


### Test Example

The easiest eay to do this is to instantiate then override the required methods of the Nop driver, for example:

```python

from app.server import create_app
from app.services.store.drivers import NopStore

def test_for_getting_a_record():
    """
    Hyperthetical test where our app needs to get a record from the "Store"
    to test some other piece of fuctionality.
    """
    mock_store = NopStore()
    nop_store.get_record = lambda: {"mock": "record"}

    app = create_app(store=mock_store)
    # do your test

```

Note: You'll need to use the `NopX` driver implementations rather than `mock.Mock()` as the `create_app` constructor is checking to make sure the **every driver is inherititing from its expected base class**.