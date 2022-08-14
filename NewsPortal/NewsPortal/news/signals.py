from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from .models import *


@receiver(signal=m2m_changed, sender=PostCategory,)
def mail_from_subscribers(instance, action, **kwargs):
    if action == 'post_add':
        for cat in instance.postCategory.all():
            for sub in UserCategory.objects.filter(subCategory=cat):
                msg = EmailMultiAlternatives(
                    subject=instance.title,
                    from_email='soulbrightproject@mail.ru',
                    to=[sub.subUser.email],
                )
                html_content = render_to_string(
                    'subscribe_message.html',
                    {
                        'post': instance,
                        'sub': sub,
                    }
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()
