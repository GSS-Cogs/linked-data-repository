import base64
import configparser
from pathlib import Path
from typing import Union


DEFAULT_PATH = Path(Path(__file__).parent.parent.parent / "configuration.ini")


def get_config(config_path: Union[str, Path]):
    """
    Returns the basic parsed configuration.ini
    """
    if not isinstance(config_path, (str, Path)):
        raise ValueError("get_config requires an argument of type Path or str")

    if isinstance(config_path, str):
        config_path = Path(config_path)
    assert config_path.exists(), f"Specified config ini {config_path.absolute()} does not exist"

    config = configparser.ConfigParser()
    config.read(config_path)

    # TODO: it'd be nice to suck in any ENV_VARS while we're at it.

    return config
