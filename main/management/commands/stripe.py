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


        liab = ClassLearner.objects.filter(
            no_pay=False, is_subscription=False
        ).exclude(
            status='refund',
        ).exclude(
            paid_status__gte=2,
        ).aggregate(Sum('amount'))
        total_liability = liab['amount__sum']

        liab = ClassLearner.objects.filter(
            no_pay=False, is_subscription=True
        ).exclude(
            status='refund',
        ).aggregate(Sum('ready_pay'))
        total_liability += liab['ready_pay__sum']

        paid_classes = Class.objects.filter(
            is_paid_by_teacher=True,
            is_deactivated=False,
        ).count()

        text += '\nPending balance (%s): ' % x['pending'][0]['currency']
        text += str(x['pending'][0]['amount'] / 100)
        text += '\nFuture Liabilities (usd): %s' % total_liability
        text += '\nPaid classes (by teachers): %s' % paid_classes

        sub_statuses = {}
        for ss in stripe.Subscription.list():
            if not ss['status'] in sub_statuses:
                sub_statuses[ss['status']] = 0
            sub_statuses[ss['status']] += 1
        text += '\nSubscriptions: '
        for key, value in sub_statuses.items():
            text += f'\n {value} {key} subscriptions'
        text += '\n'

        for cl in ClassLearner.objects.filter(no_pay=False, is_subscription=True, status='active'):
            cl.update_subsciption_data()

        for ms in MembershipStudent.objects.filter(Q(status='past_due') | Q(status='active')):
            ms.update_subsciption_data()

        text += '\n Transfers to teachers (subscriptions): '

        for cl in ClassLearner.objects.filter(is_subscription=True, no_pay=False, paid_status=1, status='active').values('klass__teacher__user').annotate(Sum('ready_pay')):
            user = User.objects.get(pk=cl['klass__teacher__user'])
            if not cl['ready_pay__sum']:
                continue
            ids = []
            text += '\n %s %s (%s)' % (user.first_name, user.last_name, user.email)
            if not user.has_external_account:
                text += ' => %s' % cl['ready_pay__sum']
                text += ' (has account: %s) ' % user.has_external_account
                if not user.first_earn_date:
                    now = datetime.now(tz=timezone.utc)
                    user.first_earn_date = now
                    url = settings.FULL_URL + '/dashboard/teach/account_take'
                    cl_sum = cl['ready_pay__sum']
                    notif_text = f'Text notification:  Teachbeach: You’ve got ${cl_sum} {url}'
                    send_text(notif_text, user.phone)
                    user.save()
            else:
                with transaction.atomic():
                    subs_amount = 0
                    for cl_item in ClassLearner.objects.filter(is_subscription=True, no_pay=False, paid_status=1, status='active', klass__teacher__user=user):
                        cl_item.total_paid += cl_item.ready_pay
                        subs_amount += cl_item.ready_pay
                        cl_item.ready_pay = 0
                        ids.append(cl_item.pk)
                        cl_item.save()
                    text += ' => %s' % subs_amount
                    text += ' (has account: %s) ' % user.has_external_account


                    acc = stripe.Account.retrieve(user.stripe_account_id)
                    if not acc['payouts_enabled']:
                        text += ' Payment failed. Missed requirements: %s' % acc['requirements']
                        continue
                    x = stripe.Transfer.create(
                        amount=int(subs_amount*100),
                        currency="usd",
                        destination=user.stripe_account_id,
                    )
                    pay = Payment(
                        user=user,
                        amount=subs_amount,
                        payment_id=x['id'],
                    )
                    pay.save()
                    ClassLearner.objects.filter(
                        pk__in=ids,
                        klass__teacher__user=user,
                    ).update(payments=CombinedExpression(F('payments'), '||', Value([pay.pk])))
                    text += ' PAID '


        for cl in ClassLearner.objects.filter(no_pay=False, paid_status=1, status='succeeded'):
            try:
                x = stripe.Charge.retrieve(cl.session_id)
            except stripe.error.InvalidRequestError:
                text += '\nid=%s is for test mode' % cl.id
                continue
            if x.refunded:
                cl.status = 'refund'
                cl.save()
            if not x.paid:
                text += '\nCheck transaction %s: %s' % (cl.session_id, x['outcome']['seller_message'])
                cl.paid_status = 3
                cl.save()

        text += '\n Transfers to teachers: '

        for cl in ClassLearner.objects.filter(is_subscription=False, no_pay=False, paid_status=1, status='succeeded').values('klass__teacher__user').annotate(Sum('amount')):
            user = User.objects.get(pk=cl['klass__teacher__user'])
            text += '\n %s %s (%s)' % (user.first_name, user.last_name, user.email)
            text += ' => %s' % cl['amount__sum']
            text += ' (has account: %s) ' % user.has_external_account

            if not user.has_external_account and not user.first_earn_date:
                now = datetime.now(tz=timezone.utc)
                user.first_earn_date = now
                url = settings.FULL_URL + '/dashboard/teach/account_take'
                cl_sum = cl['amount__sum']
                notif_text = f'Text notification:  Teachbeach: You’ve got ${cl_sum} {url}'
                send_text(notif_text, user.phone)
                user.save()

            if user.has_external_account:
                acc = stripe.Account.retrieve(user.stripe_account_id)
                if not acc['payouts_enabled']:
                    text += ' Payment failed. Missed requirements: %s' % acc['requirements']
                    continue
                x = stripe.Transfer.create(
                    amount=int(cl['amount__sum']*100),
                    currency="usd",
                    destination=user.stripe_account_id,
                    # transfer_group="payout123"
                )
                # print(x)
                pay = Payment(
                    user=user,
                    amount=cl['amount__sum'],
                    payment_id=x['id'],
                )
                pay.save()
                ClassLearner.objects.filter(
                    no_pay=False, paid_status=1, status='succeeded',
                    klass__teacher__user=user,
                ).update(payment=pay.pk, paid_status=2)
                text += ' PAID '

        print(text)
        email_list = ['alisacromer@gmail.com', ]
        send_mail(
            'Information about payments',  # subject
            text,  # body
            settings.DEFAULT_FROM_EMAIL,
            email_list,
            fail_silently=False,
        )
