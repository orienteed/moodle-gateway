from datetime import datetime
from logs.setup import logger
import os


def remove_url(object_to_clean):
    if isinstance(object_to_clean, dict):
        for key, value in object_to_clean.items():
            if isinstance(value, str) and os.getenv("MOODLE_URL_DOCKER") in value:
                object_to_clean[key] = object_to_clean[key].replace(os.getenv("MOODLE_URL_DOCKER"), "")
            elif isinstance(value, (list, dict)):
                remove_url(value)
    elif isinstance(object_to_clean, list):
        for item in object_to_clean:
            if isinstance(item, (list, dict)):
                remove_url(item)


def format_output(json_data):
    logger.info("INFO    - [" + str(datetime.now()) + "]: Formatting output to remove Moodle URL")
    remove_url(json_data)
    logger.info("INFO    - [" + str(datetime.now()) + "]: Output formatted successfully")
    return json_data
