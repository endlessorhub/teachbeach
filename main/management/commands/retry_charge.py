import os
import stripe
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

from main.models import Class, PaymentByTeacher, User, UserCard


class Command(BaseCommand):
    help = 'charge teachers'

    def handle(self, *args, **options):
        stripe.api_key = os.environ['STRIPE_SECRET_KEY']

        teachers = {}
        text = ''
        text += ' Retry charge teachers (just testing, no real charges yet): \n\n'

        for c in PaymentByTeacher.objects.filter(status='retry').order_by('-created_at'):
            u = User.objects.get(pk=c.user_id)

            try:
                uc = UserCard.objects.get(user=u)
            except UserCard.DoesNotExist:
                text += f"{u.first_name} {u.email} (id: {u.id}) charged ${c.amount}. Result: does not have card\n"
                email_body = f"Hi {u.email}. You don't have card linked to account. All your classes are paused now."
                # email_list = [t.user.email, 'alisacromer@teachbeach.com'],
                email_list = ['alisacromer@teachbeach.com', 'voronp@gmail.com']
                send_mail(
                    'TEST. Teachbeach. Retry charge failed',  # subject
                    email_body,  # body
                    settings.DEFAULT_FROM_EMAIL,
                    email_list,
                    fail_silently=True,
                )
                c.status = 'retry_failed'
                c.save()
                continue

                text += f"{u.first_name} {u.email} (id: {u.id}) charged ${c.amount}. Result: {status}\n"

            # charge_id = ''
            # pay = PaymentByTeacher(
            #     charge_id=charge_id,
            #     classes=data['ids'],
            #     amount=data['amount'] * 100,
            #     status=status,
            # )
            # pay.save()

        print(text)
        email_list = ['voronp@gmail.com', 'alisacromer@gmail.com']
        send_mail(
            'Retry charge teachers',  # subject
            text,  # body
            settings.DEFAULT_FROM_EMAIL,
            email_list,
            fail_silently=False,
        )
