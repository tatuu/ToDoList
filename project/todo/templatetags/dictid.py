from django import template

register = template.Library()

@register.filter(name='dictid')
def dictid(value, arg, default=""):
    if arg in value:
        return value[arg]
    else:
        return default