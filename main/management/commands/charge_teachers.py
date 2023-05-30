import os
import stripe
from datetime import datetime, timedelta
from monthdelta import monthdelta

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

from main.models import Class, PaymentByTeacher, Teacher, UserCard


class Command(BaseCommand):
    help = 'charge teachers'

    def handle(self, *args, **options):
        stripe.api_key = os.environ['STRIPE_SECRET_KEY']

        teachers = {}
        for c in Class.objects.filter(is_paid_by_teacher=True, is_deactivated=False, teacher__user__is_free_member=False):
            teachers.setdefault(c.teacher.pk, {'amount': 0, 'ids': []})
            days_delta = datetime.now() - c.activated_at.replace(tzinfo=None)
            if not days_delta.days:
                continue
            if (c.activated_at.replace(tzinfo=None) + monthdelta(1)) <= datetime.now():
                teachers[c.teacher.pk]['amount'] += 500
            else:
                x = int(500 * days_delta.days / 30.0)
                teachers[c.teacher.pk]['amount'] += x
            teachers[c.teacher.pk]['ids'].append(c.id)
        text = ''
        text += ' Charge teachers: \n\n'
        for t_id, data in teachers.items():
            if data['amount'] > 0:
                t = Teacher.objects.get(pk=t_id)
                has_customer = True
                try:
                    uc = UserCard.objects.get(user=t.user)
                except UserCard.DoesNotExist:
                    has_customer = False

                if has_customer and not uc.customer_id:
                    has_customer = False

                if not has_customer:
                    text += f"{t.first_name} {t.user.email} (id: {t.id}) charged ${data['amount']/100}. Result: does not have card\n"
                    email_body = f"Hi {t.user.first_name}. \n\nYou don't have card linked to account. Please add your card or your classes will be disabled.\n {settings.FULL_URL}/dashboard/teach/account_make"
                    email_list = [t.user.email, 'alisa@teachbeach.com']
                    send_mail(
                        'Teachbeach. Charge failed',  # subject
                        email_body,  # body
                        settings.DEFAULT_FROM_EMAIL,
                        email_list,
                        fail_silently=True,
                    )
                    status = 'retry'
                    charge_id = ''
                    pay = PaymentByTeacher(
                        charge_id=charge_id,
                        classes=data['ids'],
                        amount=data['amount'],
                        status=status,
                        user=t.user,
                    )
                    pay.save()
                    continue

                # actual charge
                charge = None
                try:
                    desc = 'Teachbeach. Monthly charge.'
                    charge = stripe.Charge.create(
                        amount=data['amount'],
                        currency='usd',
                        description=desc,
                        customer=uc.customer_id,
                    )
                    status = charge['status']
                except stripe.error.CardError as e:
                    status = 'retry'
                    pay = PaymentByTeacher(
                        charge_id='',
                        classes=data['ids'],
                        amount=data['amount'],
                        status='retry',
                        user=t.user,
                    )
                    pay.save()
                    text += f"{t.first_name} {t.user.email} (id: {t.id}) charged ${data['amount']/100}. Result: {e.user_message}\n"

                    email_body = f"Hi {t.user.first_name}. Your payment for teachbeach failed. Error: {e.user_message}. Please check you card or your classes will be disabled.\n {settings.FULL_URL}/dashboard/teach/account_make"
                    # email_list = [t.user.email, 'alisacromer@teachbeach.com'],
                    email_list = [t.user.email, 'alisa@teachbeach.com']
                    send_mail(
                        'Teachbeach. Charge failed',  # subject
                        email_body,  # body
                        settings.DEFAULT_FROM_EMAIL,
                        email_list,
                        fail_silently=True,
                    )
                    continue

                pay = PaymentByTeacher(
                    charge_id=charge['id'],
                    classes=data['ids'],
                    amount=data['amount'],
                    status=status,
                    user=t.user,
                )
                pay.save()

                send_mail(
                    'Teachbeach: Classes monthly fee',  # subject
                    f"Your card has been charged (${data['amount']/100}). Thank you for using Teachbeach.",  # body
                    settings.DEFAULT_FROM_EMAIL,
                    [t.user.email, ],
                    fail_silently=True,
                )

                text += f"{t.first_name} {t.user.email} (id: {t.id}) charged ${data['amount']/100}. Result: {status}\n"

        print(text)
        email_list = ['voronp@gmail.com', 'alisacromer@gmail.com']
        send_mail(
            'Charge teachers',  # subject
            text,  # body
            settings.DEFAULT_FROM_EMAIL,
            email_list,
            fail_silently=False,
        )
