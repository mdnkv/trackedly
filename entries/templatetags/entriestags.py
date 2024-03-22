from django import template
from entries.utils import map_entry_as_duration

register = template.Library()


@register.filter(name='get_entry_duration')
def get_entry_duration(entry):
    return map_entry_as_duration(entry)
