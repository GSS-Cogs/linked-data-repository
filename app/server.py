from configparser import ConfigParser
from pathlib import Path
import random
from typing import Union, TypeVar

from kink import inject
from sanic import Sanic, json

from app.services import interfaces, configure_services
from app.utils import get_config

T = TypeVar("T")


@inject
def _boostrap_app(
    config: ConfigParser,
    name: str,
    store: interfaces.Store,
    messenger: interfaces.Messenger,
    sanic_test_mode: bool = False,
) -> (Sanic):
    """
    Bootstraps Sanic application with directly injected services,
    you should never need to directly pass in any of the interfaces.<X>
    positional arguments.

    :sanic_test_mode:       toggles Sanics default behaviour of caching
                            instanitated app instances.
    """

    Sanic.test_mode = sanic_test_mode
    app = Sanic(name=name)
    app.ctx.config = config

    # Confirm di services match required protocols
    msg = "{} does not implemented protocol interface {}"
    for service_implemented, service_interface in {
        store: interfaces.Store,
        messenger: interfaces.Messenger,
    }.items():
        assert isinstance(service_implemented, service_interface), msg.format(
            service_implemented, service_interface
        )

    # Assign services to app
    app.ctx.store = store
    app.ctx.messenger = messenger

    return app


def create_app(
    name=str("_" + str(random.randint(0, 10000))),
    store: Union[interfaces.Store, str, None] = None,
    messenger: Union[interfaces.Messenger, str, None] = None,
    sanic_test_mode: bool = False,
    config_path: Union[Path, str] = Path(Path(__file__).parent / "configuration.ini")
) -> (Sanic):
    """
    Constructor for configuring the app and dependencies prior to calling the 
    principle app constructor.
    """
    # App config
    config = get_config(config_path)

    # Configure di container
    service_map = {"store": store, "messenger": messenger}
    configure_services(config, **service_map)

    # Bootstrap the app
    app = _boostrap_app(config, name, sanic_test_mode=sanic_test_mode)

    return app


if __name__ == "__main__":

    app = create_app(name="api")

    # TODO - views should probably be attached in their own file(s) to keep things clean.
    @app.add_route("/")
    async def home(request):
        return json({"just some": "holding text"})

    app.run(host="0.0.0.0", port=3000, debug=True, access_log=True)
