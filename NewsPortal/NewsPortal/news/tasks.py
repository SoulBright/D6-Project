from django_apscheduler.models import DjangoJobExecution
from NewsPortal.settings import DEFAULT_FROM_EMAIL

from datetime import timedelta, date

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import *


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def newsletter_mail_for_the_week():
    week = timedelta(days=7)
    past_week_posts = []
    for cat in Category.objects.all():
        post = PostCategory.objects.filter(categoryThrough=cat)
        for p in post:
            creation = date.today() - p.postThrough.dateCreation.date()
            if creation < week:
                past_week_posts.append(p)
        for sub in UserCategory.objects.filter(subCategory=cat):
            msg = EmailMultiAlternatives(
                subject=f'Контент за неделю в категории {cat}',
                from_email=DEFAULT_FROM_EMAIL,
                to=[sub.subUser.email],
            )
            html_content = render_to_string(
                'subscribe_massage_weekly.html',
                {
                    'post': post,
                    'sub': sub,
                    'past_week_posts': past_week_posts
                }
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()
