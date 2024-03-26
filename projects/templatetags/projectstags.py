from django import template
from entries.utils import get_total_duration

register = template.Library()


@register.filter(name='get_project_duration')
def get_project_duration(project):
    entries = project.entries.all()
    duration = get_total_duration(entries)
    return duration
