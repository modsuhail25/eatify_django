from django import template

register = template.Library()

@register.filter()
def to_str(value):
    return str(value)

@register.filter
def dict_key(d, key):
    """Fetch value from dictionary using a key."""
    try:
        return d.get(str(key), "")  # Ensure key is a string
    except AttributeError:
        return ""