import os


def get_api_key(api_name: str):
    is_github_action = False
    key = ""

    try:
        if os.environ["IS_GITHUB_ACTION"]:
            is_github_action = bool(os.getenv("IS_GITHUB_ACTION"))

    except KeyError:
        pass

    if is_github_action:
        if api_name == "OPEN_DART_KEY":
            key = os.getenv("OPEN_DART_KEY")
        else:
            key = os.getenv("PUBLIC_DATA_PORTAL")

    else:
        import config.api_key

        if api_name == "OPEN_DART_KEY":
            key = config.api_key.OPEN_DART_KEY

        else:
            key = config.api_key.PUBLIC_DATA_PORTAL

    return key
