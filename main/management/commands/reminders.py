import os
import stripe
import pytz
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from main.models import (
    GroupEnroll,
    PrivateEnroll,
    SubCategory,
    ClassLearner,
    User,
    Class,
)
import time
from datetime import datetime, timedelta
from main.utils import send_text
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Cron reminders'

    def handle(self, *args, **options):
        now = datetime.now(tz=timezone.utc)

        # now = datetime(2019,7,29,20,47)
        # now = timezone.utc.localize(now)

        # reject all requested without response after 48 hours
        enr = PrivateEnroll.objects.filter(
            time_from_gmt__lt=now-timedelta(hours=48),
            status='requested',
        )
        for x in enr:
            x.status = 'rejected'
            x.decline_reason = 'Not approved before requested time'
            x.save()
            # do refund
            any_approved = PrivateEnroll.objects.filter(
                order=x.order,
                status='approved',
            ).count()
            if not any_approved:
                c = x.order

                if not c.no_pay and c.status == 'succeeded' and c.session_id:
                    stripe.api_key = os.environ['STRIPE_SECRET_KEY']

                    s = stripe.Charge.retrieve(c.session_id)

                    refund = stripe.Refund.create(
                        charge=c.session_id,
                    )

                    c.status = 'refund'
                    c.save()
                    category = ''
                    if c.klass.subcategories:
                        subc = SubCategory.objects.get(pk=c.klass.subcategories[0])
                        category = subc.name

                        link = settings.FULL_URL + '/learners/search/online/none/%s/%s' % (
                            subc.category.pk,
                            subc.pk,
                        )
                    else:
                        link = settings.FULL_URL + '/learners/search/online/none'

                    text = f"{c.amount_full} has be credited to your account. Keep learning! Here our top {category} teachers. {link}"

                    if c.user.phone:
                        send_text(
                            text,
                            c.user.phone
                        )
                    send_mail(
                        'Teachbeach Refund',  # subject
                        text,  # body
                        settings.DEFAULT_FROM_EMAIL,
                        [c.user.email],
                        fail_silently=True,
                    )

        # 24 hours before private lesson
        next_day = now + timedelta(hours=24)
        enr = PrivateEnroll.objects.filter(
            time_from_gmt__gt=now+timedelta(hours=12),
            time_from_gmt__lte=next_day,
            status='approved',
            notification_sent=False,
            order__klass__is_deactivated=False,
        ).distinct('order__klass')
        for x in enr:
            class_tz = x.order.klass.get_timezone()
            klass = x.order.klass
            # teacher
            # link = settings.FULL_URL + '/dashboard/teach/classes'  # % c.klass.pk
            text = 'Reminder: %s with %s is tomorrow at %s %s' % (
                klass.name,
                x.order.user,
                x.time_from,
                class_tz,
            )

            if klass.teacher.user.phone:
                send_text(
                    text,
                    klass.teacher.user.phone
                )
            send_mail(
                'Teachbeach Reminder',  # subject
                text,  # body
                settings.DEFAULT_FROM_EMAIL,
                [klass.teacher.user.email],
                fail_silently=True,
            )

            # student:
            if (klass.teacher.user.is_company and klass.teacher.user.company.reminder_day) or (not klass.teacher.user.is_company and klass.teacher.reminder_day):
                link = settings.FULL_URL + '/dashboard/learn/classes'
                text = 'Teachbeach Reminder: You have %s with %s scheduled tomorrow at %s %s. %s' % (
                    klass.name,
                    klass.teacher.first_name,
                    x.time_from,
                    class_tz,
                    link,
                )
                send_mail(
                    'Teachbeach Reminder',  # subject
                    text,  # body
                    settings.DEFAULT_FROM_EMAIL,
                    [x.order.user.email],
                    fail_silently=True,
                )

            # mark as sent
            PrivateEnroll.objects.filter(
                order__klass=klass,
                time_from_gmt__gt=now,
                time_from_gmt__lte=next_day,
                status='approved',
                notification_sent=False,
                order__klass__is_deactivated=False,
            ).update(notification_sent=True)

        # 30 minutes before group - for teacher
        next_30min = now + timedelta(minutes=30)
        enr = GroupEnroll.objects.filter(
            time_from_gmt__gt=now,
            time_from_gmt__lte=next_30min,
            status='approved',
            notification_sent=False,
            order__klass__is_deactivated=False,
        ).distinct('order__klass')
        for x in enr:
            klass = x.order.klass
            # link = settings.FULL_URL + '/dashboard/teach/classes'  # % c.klass.pk
            text = 'Reminder: %s will begin in 30 minutes' % (
                klass.name
            )
            if klass.teacher.user.phone:
                send_text(
                    text,
                    klass.teacher.user.phone
                )
            send_mail(
                text,  # subject
                text,  # body
                settings.DEFAULT_FROM_EMAIL,
                [klass.teacher.user.email],
                fail_silently=True,
            )

            # mark as sent
            GroupEnroll.objects.filter(
                order__klass=klass,
                time_from_gmt__gt=now,
                time_from_gmt__lte=next_30min,
                status='approved',
                notification_sent=False,
                order__klass__is_deactivated=False,
            ).update(notification_sent=True)

        # 10 minutes before private - for student
        next_10min = now + timedelta(minutes=10)
        next_5min = now + timedelta(minutes=5)
        enr = PrivateEnroll.objects.filter(
            time_from_gmt__gt=next_5min,
            time_from_gmt__lte=next_10min,
            status='approved',
            order__klass__is_deactivated=False,
        )
        for x in enr:
            class_tz = x.order.klass.get_timezone()
            class_tz = pytz.timezone(class_tz)
            dt = class_tz.localize(x.time_from_gmt)
            link = settings.FULL_URL + '/dashboard/learn/classes'
            text = """It’s sunny! %s with %s begins in ten minutes on %s, %s %s.

Powered by TeachBeach
""" % (
                x.order.klass,
                x.order.klass.teacher.first_name,
                dt.strftime('%A'),
                x.time_from,
                class_tz,
            )
            if (x.order.klass.teacher.user.is_company and x.order.klass.teacher.user.company.reminder_10min) or (not x.order.klass.teacher.user.is_company and x.order.klass.teacher.reminder_10min):
                if x.order.user.phone:
                    send_text(
                        text,
                        x.order.user.phone
                    )
                send_mail(
                    'Teachbeach Reminder',  # subject
                    text,  # body
                    settings.DEFAULT_FROM_EMAIL,
                    [x.order.user.email],
                    fail_silently=True,
                )

        # 2 hour after lesson complete - if more in package - for student
        prev_120min = now - timedelta(minutes=120)
        prev_125min = now - timedelta(minutes=125)
        enr = PrivateEnroll.objects.filter(
            time_from_gmt__gt=prev_125min,
            time_from_gmt__lte=prev_120min,
            status='approved',
            order__klass__is_deactivated=False,
        )
        for x in enr:
            has_more = PrivateEnroll.objects.filter(
                order=x.order,
                time_from_gmt__gt=now,
                status='approved'
            ).count()
            if has_more:
                continue
            credits = x.order.num_lessons - x.order.reserved_lessons
            if credits > 0:
                link = settings.FULL_URL + '/dashboard/learn/classes'
                text = """Hi %s.

Congrats on completing your %s session! You have %s credits left. 
Add more dates at %s 

All the best, 

%s
%s
%s 
Powered by TeachBeach
""" % (
                    x.order.user.first_name,
                    x.order.klass,
                    credits,
                    link,
                    x.order.klass.teacher.first_name,
                    x.order.klass.teacher.phone or x.order.klass.teacher.user.phone,
                    x.order.klass.teacher.email or x.order.klass.teacher.user.email,
                )
            if credits == 0:
                link = settings.FULL_URL + '/company/%s' % x.order.klass.teacher.user.company.slug if x.order.klass.teacher.user.is_company else settings.FULL_URL + '/class/%s' % x.order.klass.pk
                text = """Hi %s, 

Congrats on completing %s. You are on a roll!  You are invited to keep learning: %s

All the best, 

%s
%s
%s 
Powered by TeachBeach
""" % (
                    x.order.user.first_name,
                    x.order.klass,
                    link,
                    x.order.klass.teacher.first_name,
                    x.order.klass.teacher.phone or x.order.klass.teacher.user.phone,
                    x.order.klass.teacher.email or x.order.klass.teacher.user.email,
                )
            if (x.order.klass.teacher.user.is_company and x.order.klass.teacher.user.company.reminder_renew) or (not x.order.klass.teacher.user.is_company and x.order.klass.teacher.reminder_renew):
                if x.order.user.phone:
                    send_text(
                        text,
                        x.order.user.phone
                    )
                send_mail(
                    'Congrats on completing classes',  # subject
                    text,  # body
                    settings.DEFAULT_FROM_EMAIL,
                    [x.order.user.email],
                    fail_silently=True,
                )

        # 1 hour after order to student if no date selected
        prev_60min = now - timedelta(minutes=60)
        prev_65min = now - timedelta(minutes=65)
        orders = ClassLearner.objects.filter(
            created_at__gt=prev_65min,
            created_at__lte=prev_60min,
        )
        for order in orders:
            if not PrivateEnroll.objects.filter(order=order).count() and \
                    not GroupEnroll.objects.filter(order=order).count():

                link = settings.FULL_URL + '/dashboard/learn/classes'
                text = 'Thanks for your payment! Please schedule a time for your classes with %s: %s  ' % (
                    order.klass.teacher.first_name,
                    link,
                )
                send_mail(
                    'Teachbeach: New order',  # subject
                    text,  # body
                    settings.DEFAULT_FROM_EMAIL,
                    [order.user.email, ],
                    fail_silently=True,
                )
                if order.user.phone:
                    send_text(
                        text,
                        order.user.phone
                    )

        # 1 hour after user registration
        new_users = User.objects.filter(
            date_joined__gt=prev_65min,
            date_joined__lte=prev_60min,
            class_id__isnull=False,
        )
        for u in new_users:
            try:
                c = Class.objects.get(pk=u.class_id)
            except:
                continue
            text = f"{u.first_name} is checking out your {c.name} lesson. Contact them at {u.email}, {u.phone}. "
            send_mail(
                'Teachbeach: Notification',  # subject
                text,  # body
                settings.DEFAULT_FROM_EMAIL,
                [c.teacher.user.email, ],
                fail_silently=True,
            )
