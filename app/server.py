import random
from typing import Union

from sanic import Sanic, json

from app.services import Composer, BaseMessager, BaseStore

# TODO - once merged with a/the pr containing configuration handling,
# take the default str arguments for services from configuration.
def create_app(
    name: str = str("_" + str(random.randint(0, 10000))),
    store: Union[str, BaseStore] = "Nop",
    messager: Union[str, BaseMessager] = "Nop",
    sanic_test_mode: bool = False,
    enforce_base_classes: bool = True,
) -> (Sanic):
    """
    Instantiates Sanic application.

    Services can be specified via keyword str arguments that map to
    service implementation as per app.services.inventory, or by passing
    in instantiated classes extending the relevant BaseX classes.

    :sanic_test_mode:       toggles Sanics default behaviour of caching
                            instanitated app instances
    :enforce_base_classes:  disables type check agaisnt expected base class
                            (so mock.Mocks() can be passed in if needed).
    """

    Sanic.test_mode = sanic_test_mode
    app = Sanic(name=name)

    # TODO: holding value, use actual config (once merged with a PR that contains some)
    config = ""
    
    # Adding services to app.ctx
    composer = Composer(config, enforce_base_classes)
    app.ctx.store = composer.store(store)
    app.ctx.messager = composer.messager(messager)

    return app


if __name__ == "__main__":

    app = create_app(name="api")

    # TODO - views should probably be attached in their own file(s) to keep things clean.
    @app.add_route("/")
    async def home(request):
        return json({"just some": "holding text"})

    app.run(host="localhost", port=3000, debug=True, access_log=True)
