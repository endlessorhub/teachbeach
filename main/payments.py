import os
import stripe
from django.core.mail import send_mail
from django.conf import settings
from .models import PaymentByTeacher, UserCard, Class

stripe.api_key = os.environ['STRIPE_SECRET_KEY']


def charge_for_class(klass:Class, user, is_draft=False):
    COST_OF_CLASS = 500  # in cents
    class_id = None
    if klass:
        class_id = klass.pk
        desc = 'Teachbeach. Charge for class: %s' % klass
    else:
        desc = 'Teachbeach. Charge for added class'
    try:
        uc = UserCard.objects.get(user=user)
    except UserCard.DoesNotExist:
        return {'success': False, 'error_message': 'Please add a payment method'}

    if not uc.customer_id:
        return {'success': False, 'error_message': 'Please add a payment method'}
    charge = None
    try:
        charge = stripe.Charge.create(
            amount=COST_OF_CLASS,
            currency='usd',
            description=desc,
            customer=uc.customer_id,
        )
    except stripe.error.CardError as e:
        return {'success': False, 'error_message': e.user_message}

    pay = PaymentByTeacher(
        charge_id=charge['id'],
        status=charge['status'],
        amount=COST_OF_CLASS,
        single_class=class_id,
        is_draft=is_draft,
        user=user,
    )
    pay.save()

    if is_draft:
        class_name = klass.class_data['teacherGroupClass']['privateClassName'] if klass.class_data['teacherLessonType'] == 'private' else klass.class_data['teacherGroupClass']['groupClassName']
    else:
        class_name = klass.private_className if klass.is_private else klass.name

    send_mail(
        'It’s sunny! Your class has been activated!',  # subject
        """Hi %s, 

“%s” has been published. Thank you for choosing TeachBeach, the fun way to earn and learn.
The charge this month is $5. 
Manage your class at %s/dashboard/teach/classes 
For concierge service, please call 408.892.9815.
Cheers, 
Alisa
""" % (
            user.first_name,
            class_name,
            settings.FULL_URL,
        ),  # body
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )

    return {
        'success': True,
        'pay_id': pay.pk,
    }

def update_payment(pay_id, class_id):
    pay = PaymentByTeacher.objects.get(pk=pay_id)
    pay.single_class=class_id
    pay.is_draft = False
    pay.save()
