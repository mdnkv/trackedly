from django.core.mail import send_mail
from django.template.loader import get_template


def send_confirmation_email(user, token):
    data = {'token_id': str(token.pk)}
    message = get_template('users/emails/confirmation_email.txt').render(data)
    send_mail(
        subject='Trackedly email confirmation',
        message=message,
        from_email='no-reply@trackedly.com',
        recipient_list=[user.email],
        fail_silently=True
    )

