url = "demo-moodle"


def remove_url(object_to_clean):
    if isinstance(object_to_clean, dict):
        for key, value in object_to_clean.items():
            if isinstance(value, str) and url in value:
                object_to_clean[key] = ""
            elif isinstance(value, (list, dict)):
                remove_url(value)
    elif isinstance(object_to_clean, list):
        for item in object_to_clean:
            if isinstance(item, (list, dict)):
                remove_url(item)


def format_output(json_data):
    remove_url(json_data)
    return json_data
