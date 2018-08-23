import os


def to_bool(s, *, strict=True):
    if s is None:
        return None
    if isinstance(s, bool):
        return s
    if isinstance(s, str) and len(s):
        if strict:
            if s.lower() in ("f", "false", "n", "no", "0"):
                return False
        else:
            if s[0].lower() in ("f", "n", "0"):
                return False
        return True
    return False


def get_bool_from_env(name, default):
    return to_bool(os.environ.get(name, default))


DEBUG = get_bool_from_env("DEBUG", False)
COLORS = get_bool_from_env("COLORS", None)
