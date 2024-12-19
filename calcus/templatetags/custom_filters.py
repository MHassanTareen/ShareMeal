from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtracts the arg from value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0
