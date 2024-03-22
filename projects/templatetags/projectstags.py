from django import template
from datetime import timedelta
from entries.utils import map_entry_as_duration

register = template.Library()



@register.filter(name='get_project_duration')
def get_project_duration(project):
    entries_durations = list(map(lambda entry: map_entry_as_duration(entry), project.entries.all()))
    total = timedelta()
    for e in entries_durations:
        total += e
    return total
