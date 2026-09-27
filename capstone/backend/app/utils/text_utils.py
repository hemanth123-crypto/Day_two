import re


def normalize_space(value):
    if value is None:
        return ''
    value = str(value)
    return re.sub(r'\s+', ' ', value).strip()


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_lower_key(value):
    if value is None:
        return ''
    return str(value).lower().strip()
