import os
from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.db.models.expressions import CombinedExpression, Value

from django.core.management.base import BaseCommand
from django.db.models import Sum
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

        for ms in MembershipStudent.objects.filter(status='active'):
            ms.update_subsciption_data()

        print('done')
