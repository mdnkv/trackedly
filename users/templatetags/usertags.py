from django import template
from hashlib import md5

register = template.Library()


@register.filter(name='get_gravatar_url')
def get_gravatar_url(user):
    hashed_email = md5(user.email.encode())
    return f"https://www.gravatar.com/avatar/{hashed_email.hexdigest()}?d=identicon"
