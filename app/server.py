import inspect
import random
from typing import Union

from sanic import Sanic, json

from app.services import compose, BaseMessager, BaseStore

# TODO - once merged with a/the pr containing configuration handling,
# also take the default str arguments for drivers from the configuration.ini.
def create_app(
    name: str = str("_" + str(random.randint(0, 10000))),
    store: Union[str, BaseStore] = 'Nop',
    messager: Union[str, BaseMessager] = 'Nop',
    sanic_test_mode: bool = False,
    enforce_base_classes: bool = True
) -> (Sanic):
    """
    Instantiates Sanic application.

    Services can be specified via keyword str arguments that map to 
    drivers as specified in app.services.inventory, or by passing
    in instantiated classes extending the relevant BaseX classes.

    :sanic_test_mode:       toggles Sanics default behaviour of caching 
                            instanitated app instances
    :enforce_base_classes:  disables type check of driver base class (so 
                            test Mocks can be passed in).
    """

    Sanic.test_mode = sanic_test_mode
    app = Sanic(name=name)

    # Adding initialised drivers to app.ctx
    app.ctx.store = compose.store(store) if isinstance(store, str) else store
    app.ctx.messager = (
        compose.messager(messager) if isinstance(messager, str) else messager
    )
    
    # TODO: holding value, use actual config (once merged with a PR that contains some)
    config = ""

    for driver_in_use, driver_base_class in {
        app.ctx.store: BaseStore,
        app.ctx.messager: BaseMessager,
    }.items():

        # Assert driver has been instanitated
        assert not inspect.isclass(driver_in_use), \
            f"Driver '{driver_in_use}' is not but should have been instantiated."

        # Assert driver is extending the correct parent class
        if enforce_base_classes:
            driver_in_use_base = driver_in_use.__class__.__bases__[-1]
            if str(driver_in_use_base) != str(driver_base_class):
                raise TypeError(
                    f"Driver '{driver_in_use_base}' does not but should have parent class '{driver_base_class}'."
                )
            
        # Driver configuration
        driver_in_use.setup(config=config)

    return app


if __name__ == "__main__":

    app = create_app(name="api")

    # TODO - views should probably be attached in their own file(s) to keep things clean.
    @app.add_route("/")
    async def home(request):
        return json({"just some": "holding text"})

    app.run(host="localhost", port=3000, debug=True, access_log=True)
