import os
from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.db.models.expressions import CombinedExpression, Value

from django.core.management.base import BaseCommand
from django.db.models import Sum, Q
from django.core.mail import send_mail
from django.utils import timezone
from main.utils import send_text
import stripe
import time
from datetime import datetime
from main.models import ClassLearner, User, Payment, Class, MembershipStudent


class Command(BaseCommand):
    help = 'stripe history'

    # def add_arguments(self, parser):
    #     parser.add_argument('--confirm', action='store_true', required=True, help='Confirm that you really want to reindex all social updates. It will take a long time!')

    def handle(self, *args, **options):

        stripe.api_key = os.environ['STRIPE_SECRET_KEY']

        x = stripe.Balance.retrieve()
        text = 'Available balance (%s): ' % x['available'][0]['currency']
        text += str(x['available'][0]['amount'] / 100)

        for ms in MembershipStudent.objects.filter(Q(status='unpaid') | Q(status='canceled')):
            text += '\nCanceled membership: %s' % ms.student.email
            ms.update_subsciption_data()

        print(text)
        email_list = ['alisacromer@gmail.com', ]
        send_mail(
            'Information about payments',  # subject
            text,  # body
            settings.DEFAULT_FROM_EMAIL,
            email_list,
            fail_silently=False,
        )
