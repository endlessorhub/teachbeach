from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Sum

from main.models import ClassLearner, User

from datetime import datetime, timedelta
from django.utils import timezone
from main.utils import send_text


class Command(BaseCommand):
    help = 'Weekly cron reminders'

    def handle(self, *args, **options):

        url = settings.FULL_URL + '/dashboard/teach/account_take'
        now = datetime.now(tz=timezone.utc)

        for cl in ClassLearner.objects.filter(is_subscription=False, no_pay=False, paid_status=1, status='succeeded').values('klass__teacher__user').annotate(Sum('amount')):
            user = User.objects.get(pk=cl['klass__teacher__user'])
            cl_sum = cl['amount__sum']
            if not user.has_external_account and user.first_earn_date:
                if user.first_earn_date < now - timedelta(days=7) and \
                        user.first_earn_date > now - timedelta(days=7*5):
                    text = f'Teachbeach: Don’t forget to collect your ${cl_sum} ({url})'
                    send_text(text, user.phone)
