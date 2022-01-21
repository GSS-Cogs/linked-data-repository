import inspect
import random
from typing import Union

from sanic import Sanic, json

from app.services import compose, BaseMessager, BaseStore

wrong_driver_type_msg = "Driver '{}' does not but should have parent class '{}'."
driver_not_instaniated_msg = "Driver '{}' is not but should have been instantiated."


def create_app(
    name: str = str("_" + str(random.randint(0, 10000))),
    store: Union[str, BaseStore] = 'Nop',
    messager: Union[str, BaseMessager] = 'Nop',
    test_mode: bool = False
) -> (Sanic):
    """
    Instantiates our Sanic application.

    Services can be specified via keyword str arguments or by passing
    in instanitated classes implementing the relevant BaseX abstracts.

    This constructor also applies basic type and sanity checks.
    
    The "register" bool is used by Sanic to register and cache instantiated app 
    instances. The default behaviour is True an anyway, we're just passing a 
    bool so we can toggle this behaviour off while testing (to avoid app instance
    naming collisions). 
    """

    Sanic.test_mode = test_mode
    app = Sanic(name=name)

    # Adding initialised drivers to app.ctx
    app.ctx.store = compose.store(store) if isinstance(store, str) else store
    app.ctx.messager = (
        compose.messager(messager) if isinstance(messager, str) else messager
    )

    # Policing
    for driver_in_use, driver_base_class in {
        app.ctx.store: BaseStore,
        app.ctx.messager: BaseMessager,
    }.items():

        # Assert driver has been instanitated
        assert not inspect.isclass(driver_in_use), driver_not_instaniated_msg.format(
            driver_in_use
        )

        # Assert driver has the correct parent class
        driver_in_use_base = driver_in_use.__class__.__bases__[-1]
        if str(driver_in_use_base) != str(driver_base_class):
            raise TypeError(
                wrong_driver_type_msg.format(driver_in_use_base, driver_base_class)
            )
            
    # Driver configuration
    # TODO: pass through actual config (once merged with a PR that contains some)
    config = ""
    app.ctx.store.setup(config=config)
    app.ctx.messager.setup(config=config)

    return app


if __name__ == "__main__":

    app = create_app(name="api")

    # TODO - views should probably be attached in their own file(s) to keep things clean.
    @app.add_route("/")
    async def home(request):
        return json({"just some": "holding text"})

    # note: for development, i.e when you `pipenv run python3 ./app/server.py`
    app.run(host="localhost", port=3000, debug=True, access_log=True)
