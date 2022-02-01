from configparser import ConfigParser
from pathlib import Path
import random
from typing import Union, TypeVar

from kink import inject
from sanic import Sanic, json

from app.services import interfaces, configure_services
from app.utils import get_app_config


T = TypeVar("T")


class ProtocolError(Exception):
    """
    Raised where an implementation does not meet the required protocols.
    """

    def __init__(self, msg: str):
        self.msg = msg


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
    you should never need to directly satisfy any of the interfaces.<X>
    positional arguments.

    :sanic_test_mode:       toggles Sanics default behaviour of caching
                            instanitated app instances.
    """

    Sanic.test_mode = sanic_test_mode
    app = Sanic(name=name)
    app.ctx.config = config

    # Confirm di services match required protocols
    msg = "{} does not implemented protocols of {}"
    for service_implemented, service_interface in {
        store: interfaces.Store,
        messenger: interfaces.Messenger,
    }.items():
        if not isinstance(service_implemented, service_interface):
            raise ProtocolError(msg.format(service_implemented, service_interface))

    # Assign services to app
    app.ctx.store = store
    app.ctx.messenger = messenger

    return app


def create_app(
    name=str("_" + str(random.randint(0, 10000))),
    store: Union[interfaces.Store, str, None] = None,
    messenger: Union[interfaces.Messenger, str, None] = None,
    sanic_test_mode: bool = False,
    config_path: Union[Path, str] = Path(Path(__file__).parent / "configuration.ini"),
) -> (Sanic):
    """
    Function for configuring the app and dependencies prior to calling the
    principle app constructor.
    """
    # App config
    config = get_app_config(config_path)

    # Configure di container
    implementations_dict = {"store": store, "messenger": messenger}
    configure_services(config, implementations_dict)

    # Bootstrap the app
    app = _boostrap_app(config, name, sanic_test_mode=sanic_test_mode)

    @app.route("/")
    async def home(request):
        return json({"just some": "holding text"})

    return app
