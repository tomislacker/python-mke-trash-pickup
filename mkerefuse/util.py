import json
import logging
import logging.config
import os.path
import yaml
from lxml import html


DEFAULT_LOGGING_CONFIG = {
    'level': logging.INFO,
    'disable_existing_loggers': False,
}


class XPathObject(object):
    """Helper for importing response [X]HTML into a class instance"""

    input_properties = {}
    """Dict of keys (property names) and XPaths (to read vals from)"""

    @classmethod
    def FromHTML(cls, html_contents):
        inst = cls()
        print("Reading through {b} bytes for {c} properties...".format(
            b=len(html_contents),
            c=len(cls.input_properties)))

        tree = html.fromstring(html_contents)

        for attr_name, xpath in cls.input_properties.items():
            print("Searching for '{n}': {x}".format(
                n=attr_name,
                x=xpath))
            elements = tree.xpath(xpath)

            if not len(elements):
                print("Failed to find '{n}': {x}".format(
                    n=attr_name,
                    x=xpath))
                continue

            setattr(
                inst,
                attr_name,
                elements[0].text)

        return inst

    def __repr__(self):
        return json.dumps(
            self.__dict__,
            indent=4,
            separators=(',', ': '))

def setup_logging(
        config_path="logging.yaml",
        config_path_env="LOG_CFG_PATH"
):
    """Setup the python logger

    Args:
        config_path (str): Path to a default config file
        config_path_env (str): Env variable to specify alternate logging config
    """
    config_override = os.getenv(config_path_env, None)
    config_path = config_path if not config_override else config_override

    if os.path.exists(config_path):
        with open(config_path, "rt") as yaml_file:
            config = yaml.load(yaml_file.read())

        logging.config.dictConfig(config)
        logging.debug("Setup logging from '{}'".format(config_path))

    else:
        logging.debug("Setup logging from defaults")
        logging.basicConfig(**DEFAULT_LOGGING_CONFIG)


class LogProducer(object):
    """Simple class to add in class-oriented logging"""
    def __init__(self, subname=None):
        logger_name = ".".join([
            self.__class__.__module__,
            self.__class__.__name__
        ])

        if subname:
            logger_name += " ({})".format(subname)
        self._log = logging.getLogger(logger_name)
