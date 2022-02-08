from configparser import ConfigParser
from pathlib import Path
import random
from typing import Union

from kink import inject
from sanic import Sanic, json

from app.services import interfaces, configure_services
from app.utils import get_app_config


def create_app(
    name=str("_" + str(random.randint(0, 10000))),
    store: Union[interfaces.Store, str, None] = None,
    messenger: Union[interfaces.Messenger, str, None] = None,
    sanic_test_mode: bool = False,
    config: Union[Path, str, ConfigParser] = Path(
        Path(__file__).parent / "configuration.ini"
    ),
) -> (Sanic):
    """
    Function for configuring the app and dependencies prior to calling the
    principle app constructor.
    """

    config_parsed: ConfigParser = (
        config if isinstance(config, ConfigParser) else get_app_config(config)
    )

    # Configure di container
    implementations_dict = {"store": store, "messenger": messenger}
    configure_services(config_parsed, implementations_dict)

    # Bootstrap the app
    Sanic.test_mode = sanic_test_mode
    app = Sanic(name=name)
    app.ctx.config = config

    @app.route("/")
    @inject
    async def home(request, store: interfaces.Store):
        return json({"store is": str(type(store))})

    return app
