# mi_aplicacion/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={'class': css_class})
    return field

