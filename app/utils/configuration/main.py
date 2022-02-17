import base64
import configparser
import os
from pathlib import Path
from typing import Union

"""
Notes:

Ideally, this'd be a `class Configuration` so we can wrap ConfigParser()
with some get/set methods and some robust config validation.

Better yet, have a shared Configuration class/approach across our
python tooling.
"""

# Note - might be better of as an env var? Wouldn't need a keyword or
# default then
DEFAULT_PATH = Path(Path(__file__).parent.parent.parent / "configuration.ini")


def get_config(path: Union[str, Path] = DEFAULT_PATH):
    """
    Returns the basic parsed configuration.ini
    Adds environmet variables.
    """
    if not isinstance(path, (str, Path)):
        raise ValueError("get_config requires an argument of type Path or str")

    if isinstance(path, str):
        path = Path(path)
    assert path.exists(), f"Specified config ini {path.absolute()} does not exist"

    config = configparser.ConfigParser()
    config.read(path)

    """
    Dev note:
    Needs thought, but the neatest configuration solution might be to us the ENV
    section in the configuration.ini for default values, so we check for an env
    var override for each field - using the ini default in its absense.

    There's a fine line between convenience and obfiscation here, if we do it we may
    need logging out of sanitised variables, warnings per default use, something
    like that.... think.
    """

    # Police current MVP approach
    assert [
        "ENV"
    ] not in config.sections(), (
        "You must have an ENV namespace in your configuration.ini file."
    )
    assert len(config["ENV"].keys()) == 0, (
        "The configuration.ini section ENV must" " always be blank"
    )

    # ------------------------
    # Dynamically add env vars

    encryption_key = os.getenv("ENCRYPTION_KEY", None)
    if not encryption_key:
        encryption_key = str(base64.urlsafe_b64encode(os.urandom(32)))
    config["ENV"]["encryption_key"] = encryption_key

    # Required auth environment variables
    msg = 'Aborting, the environment variable "{}" must be set'
    for oaev_label in [
        "OAUTH_DOMAIN",
        "OAUTH_CLIENT_ID",
        "OAUTH_CLIENT_SECRET",
        "OAUTH_REDIRECT_URI",
    ]:
        oaev_val = os.getenv(oaev_label, False)
        assert oaev_val, msg.format(oaev_label)
        config["ENV"][oaev_label.lower()] = oaev_val

    return config


config = get_config()
