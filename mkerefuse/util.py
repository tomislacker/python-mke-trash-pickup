import logging
import logging.config
import os.path

from datetime import date
from datetime import datetime


DEFAULT_LOGGING_CONFIG = {
    'level': logging.INFO,
    'disable_existing_loggers': False,
}


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


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
        import yaml

        with open(config_path, "rt") as yaml_file:
            config = yaml.load(yaml_file.read())

        logging.config.dictConfig(config)

    else:
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


def pickup_to_ics(address, pickup):
    return "\n".join([
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "CALSCALE:GREGORIAN",

        # Garbage event
        "BEGIN:VEVENT",
        "SUMMARY:Garbage Pickup",
        "DTSTART;TZID={tz}:{stamp}".format(
            tz=pickup.pickup_tz,
            stamp=pickup.next_pickup_garbage.strftime("%Y%m%dT%H%M%S"),
        ),
        "DTEND;TZID={tz}:{stamp}".format(
            tz=pickup.pickup_tz,
            stamp=pickup.next_pickup_garbage.strftime("%Y%m%dT%H%M%S"),
        ),
        "LOCATION:{}".format(" ".join([
            address.house_number,
            address.direction,
            address.street_name,
            address.street_type,
        ])),
        "DESCRIPTION:Garbage pickup",
        "STATUS:CONFIRMED",
        "SEQUENCE:3",
        "BEGIN:VALARM",
        "TRIGGER:-PT10M",
        "DESCRIPTION:Pickup Reminder",
        "ACTION:DISPLAY",
        "END:VALARM",
        "END:VEVENT",

        # Recycle event
        "BEGIN:VEVENT",
        "SUMMARY:Recycle Pickup",
        "DTSTART;TZID={tz}:{stamp}".format(
            tz=pickup.pickup_tz,
            stamp=(pickup.next_pickup_recycle_after or pickup.next_pickup_recycle).strftime("%Y%m%dT%H%M%S"),
        ),
        "DTEND;TZID={tz}:{stamp}".format(
            tz=pickup.pickup_tz,
            stamp=(pickup.next_pickup_recycle_before or pickup.next_pickup_recycle).strftime("%Y%m%dT%H%M%S"),
        ),
        "LOCATION:{}".format(" ".join([
            address.house_number,
            address.direction,
            address.street_name,
            address.street_type,
        ])),
        "DESCRIPTION:Recycle pickup",
        "STATUS:CONFIRMED",
        "SEQUENCE:3",
        "BEGIN:VALARM",
        "TRIGGER:-PT10M",
        "DESCRIPTION:Pickup Reminder",
        "ACTION:DISPLAY",
        "END:VALARM",
        "END:VEVENT",
        "END:VCALENDAR",
    ])
