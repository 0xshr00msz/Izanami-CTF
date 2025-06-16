"""
Custom template filters for the challenges app.
"""

from django import template

register = template.Library()

@register.filter
def get_dict_item(dictionary, key):
    """
    Get an item from a dictionary using the key.
    """
    return dictionary.get(key, [])
