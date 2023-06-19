from collections import Counter
import os
import re
from io import StringIO
import base64
from datetime import datetime, timedelta
from monthdelta import monthdelta
import urllib.request
import json
import stripe
import urllib
import pytz
import uuid
import csv
import time
import icalendar
import copy
import math
import decimal
import boto3
from botocore.exceptions import ClientError
from functools import reduce

from django.db.models import F, Func, Sum
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry, Point
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.core.mail import send_mail
from django.contrib.auth import get_user_model, login

from django.conf import settings
from rest_framework import viewsets, generics
from rest_framework.pagination import LimitOffsetPagination
from .models import (
    Teacher, Venue, Class, Category, SubCategory,
    ClassMedia, ClassLearner, PrivateEnroll,
    GroupEnroll, User, UserCard, Message,
    DraftClass, CompanyProfile, TeacherProfileLog,
    Newsletter, BoostMembership, EmailBoost,
    Event, MetaTag, TeacherMessage, ChargeLog,
    AddStudent, CardError, UserSettings, DeletedStudent,
    ExternalCalendar, Membership, MembershipStudent,
    Discussion, Comment
)
from .serializers import (
    TeacherSerializer, TeacherFullSerializer, VenueSerializer,
    ClassSerializer, ClassWriteSerializer, CategorySerializer, SubCategorySerializer,
    UserSerializer, ClassMediaSerializer, ClassFullSerializer,
    ClassLearnerSerializer, GlobalPackageSerializer,
    PrivateEnrollSerializer, GroupEnrollSerializer,
    PrivateEnrollDetailsSerializer, ClassShortSerializer,
    GroupEnrollDetailsSerializer, MessageSerializer,
    DraftClassSerializer, CompanyProfileSerializer,
    AddressVenueSerializer, UserShortSerializer,
    UserFutureClassesSerializer, UserAllClassesSerializer,
    NewsletterSerializer, BoostMembershipSerializer,
    EmailBoostSerializer, EventSerializer, MetaTagSerializer,
    ShortOrderSerializer, ClassLearnerNoDataClassSerializer,
    CompanyProfileWithClassesSerializer, UserSettingsSerializer,
    ManagedUserSerializer, MembershipSerializer, MembershipStudentSerializer,
    FacebookSocialAuthSerializer, GoogleSocialAuthSerializer,
    DiscussionSetupserializer, DiscussionDetailSerializer,
    CommentSerializer, DiscussionListSerializer
)
from .filters import MessageUserFilter, UserFilter

from .utils import (
    send_text, format_date_time, format_date_time_from_to,
    get_client_ip, get_message_sign, send_mail_reply_to, strip_tags
)
from .payments import charge_for_class, update_payment

from random import randrange
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from django.middleware import csrf
from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from smtplib import SMTPDataError

def get_email_company_name(class_id):
    cl = Class.objects.get(pk=class_id)
    cp = None
    if cl.teacher.user.is_company:
        cp = CompanyProfile.objects.get(user=cl.teacher.user)
    if cl.teacher.user.belongs_to:
        cp = CompanyProfile.objects.get(pk=cl.teacher.user.belongs_to)
    return cp.name+"\n" if cp else 'Teachbeach'

class MyPaginationMixin(object):

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination
        is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(
            queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given
        output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    # serializer_class = TeacherSerializer

    def get_queryset(self):
        if self.retrieve.method == 'POST':
            return get_user_model().objects.all()
        return Teacher.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserSerializer
        return TeacherFullSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def create(self, validated_data):
        user_data = validated_data.data

        try:
            tz_url = "https://maps.googleapis.com/maps/api/timezone/json?location=%s,%s&timestamp=1458000000&key=%s" % (
                user_data['lat'],
                user_data['lng'],
                os.environ['GOOGLE_MAPS_API_KEY'],
            )
            with urllib.request.urlopen(tz_url) as url:
                x = json.loads(url.read().decode())
                user_data['timezone'] = x['timeZoneId']
        except:
            user_data['timezone'] = 'US/Eastern'
        if user_data.get('first_name') and not user_data.get('last_name'):
            items = user_data.get('first_name').split(' ', 1)
            if len(items) > 1:
                user_data['first_name'] = items[0]
                user_data['last_name'] = items[1]
            else:
                user_data['last_name'] = ''
        serializer = UserSerializer(data=user_data)
        serializer.is_valid(True)
        user_data = serializer.validated_data
        user = get_user_model().objects.create_user(user_data['email'].lower(), **user_data)
        # notify admin
        send_mail(
            'TB: New user registered',  # subject
            'New user registered: %s Referred class_id: %s' % (
                user.email,
                user_data.get('class_id'),
            ),  # body
            settings.DEFAULT_FROM_EMAIL,
            ['alisacromer@gmail.com', 'debparthapratim0@gmail.com'],
            fail_silently=True,
        )
        # notify teacher
        class_id = user_data.get('class_id')
        try:
            klass = Class.objects.get(pk=class_id)
            text = f"""Congrats! {user.first_name}, {user.email}, {user.phone}, is checking out your page on Teachbeach.

Here is some text for a welcome note you can send. Just make your own edits, then cut and paste the email address and  note into a new email.

This prospect is also saved to your student list in the dashboard, so you can include them future marketing.

Hi {user.first_name},

Thanks for checking out {klass.name}.

Would love to work with you! You can text/call me any time at {klass.teacher.user.phone} for more information.

Stay safe and look forward to hearing from you!

Warmest regards,

{klass.teacher.first_name}"""
            send_mail(
                'New user registered',  # subject
                text,  # body
                settings.DEFAULT_FROM_EMAIL,
                [klass.teacher.user.email, ],
                fail_silently=True,
            )

        except Class.DoesNotExist:
            pass

        return Response(UserShortSerializer(user).data)


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class ClassMediaViewSet(viewsets.ModelViewSet):
    queryset = ClassMedia.objects.all()
    serializer_class = ClassMediaSerializer


class EventViewSet(viewsets.ViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def list(self, request):
        queryset =  Event.objects.all()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)


class UserView(generics.CreateAPIView):

    def post(self, request):
        update = False
        if request.data.get('timezone') != request.user.timezone and request.user.pk:
            request.user.timezone = request.data.get('timezone')
            update = True
        if request.data.get('phone') != request.user.phone and request.user.pk:
            request.user.phone = request.data.get('phone')
            update = True
        if request.data.get('first_name') != request.user.first_name and request.user.pk:
            request.user.first_name = request.data.get('first_name')
            update = True
        if update:
            request.user.save()
        return Response({'success': True})


class CompanyVenueView(generics.CreateAPIView):
    serializer_class = AddressVenueSerializer
    queryset = Class.objects.all()

    def get(self, request):
        addresses = Class.objects.filter(
            teaching_venue__isnull=False,
            teacher__user=request.user
        ).distinct(
            'address_google', 'address', 'address_city', 'address_zip', 'address_street',
            'address_state', 'teaching_venue', 'lat', 'lng', 'address_country'
        )
        return Response(AddressVenueSerializer(addresses, many=True).data)


class TeacherProfileView(generics.CreateAPIView):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    def get(self, request, pk=None):
        if pk:
            teacher = Teacher.objects.get(pk=pk)
            return Response(TeacherFullSerializer(teacher).data)
        else:
            if request.user.is_company:
                teachers = Teacher.objects.filter(Q(user=request.user) | Q(user__belongs_to=request.user.company.pk))
            else:
                teachers = Teacher.objects.filter(user=request.user)
            return Response(TeacherSerializer(teachers, many=True).data)

    def post(self, request):
        data = request.data
        if request.user.is_company:
            teachers = Teacher.objects.filter(Q(user=request.user) | Q(user__belongs_to=request.user.company.pk))
        else:
            teachers = Teacher.objects.filter(user=request.user)
        if not teachers:
            teacher = Teacher(
                user=request.user,
            )
            company_name = 'Teachbeach'
            admin_phone = '408.892.9815'
            admin_name = 'Alisa Cromer'
            admin_email = 'alisa@teachbeach.com'
            if request.user.belongs_to:
                root_company = CompanyProfile.objects.get(pk=request.user.belongs_to)
                company_name = root_company.name
                admin_phone = root_company.user.phone
                admin_name = root_company.user.first_name + ' ' + root_company.user.last_name
                admin_email = root_company.user.email
            subject, from_email, to = '%s Registration' % company_name, settings.DEFAULT_FROM_EMAIL, request.user.email
            text_content = render_to_string('welcome_email_text.html', {
                'first_name': request.user.first_name,
                'company_name': company_name,
                'admin_phone': admin_phone,
                'admin_name': admin_name,
                'admin_email': admin_email,
            })
            html_content = render_to_string('welcome_email.html', {
                'first_name': request.user.first_name,
                'company_name': company_name,
                'admin_phone': admin_phone,
                'admin_name': admin_name,
                'admin_email': admin_email,
            })
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to], ['alisacromer@gmail.com'])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)
        else:
            teacher = teachers[0]

        if data.get('profile'):
            if data['profile'].get('id'):
                if request.user.is_company:
                    teacher = Teacher.objects.get(
                        Q(user=request.user) | Q(user__belongs_to=request.user.company.pk),
                        Q(pk=data['profile']['id']),
                    )
                else:
                    teacher = Teacher.objects.get(
                        user=request.user,
                        pk=data['profile']['id'],
                    )
            elif request.user.is_company and teachers:
                teacher = Teacher(
                    user=request.user,
                )

            if request.user.is_company:
                teacher.first_name = data['profile'].get('first_name')
                teacher.last_name = data['profile'].get('last_name')
            else:
                if data.get('user'):
                    request.user.first_name = data['user'].get('first_name')
                    request.user.last_name = data['user'].get('last_name')
                    request.user.save()
                teacher.first_name = request.user.first_name
                teacher.last_name = request.user.last_name
            teacher.description = data['profile'].get('description')
            teacher.areas_of_specialty = data['profile'].get('areasOfSpeciality')
            teacher.email = data['profile'].get('email')
            teacher.phone = data['profile'].get('phone')
        if data.get('avatar') and data['avatar']['uploadPhoto']['imageUrl'] and data['avatar']['uploadPhoto']['imageUrl'].startswith('data:'):
            imgstr = data['avatar']['uploadPhoto']['imageUrl']
            imgname = data['avatar']['uploadPhoto']['imageName']

            _, imgstr = imgstr.split(';base64,')
            name = '%s-%s-%s' % (teacher.id, uuid.uuid1(), imgname)
            fdata = ContentFile(base64.b64decode(imgstr), name=name)
            teacher.media = fdata
            # for debug only:
            teacher.save()
            teacher.save_thumbnail()
            tpl = TeacherProfileLog(
                teacher=teacher,
                data=data,
                headers=dict(request.headers),
            )
            tpl.save()
        status = True
        err = None
        if data.get('user'):
            email = data['user']['email']
            if request.user.username.lower() != email.lower():
                if User.objects.filter(username__iexact=email):
                    status = False
                    err = 'User with this email already exists'
                else:
                    request.user.email = email
                    request.user.username = email.lower()

            request.user.first_name = data['user'].get('first_name')
            request.user.last_name = data['user'].get('last_name')
            request.user.phone = data['user'].get('phone')
            request.user.timezone = data['user'].get('timezone')
            request.user.save()
            if data['user'].get('timezone_to_classes'):
                teachers = Teacher.objects.filter(user=request.user)
                Class.objects.filter(teacher__in=teachers).update(timezone=request.user.timezone)

        teacher.save()
        return Response({'success': status, 'id': teacher.pk, 'err': err})


class CompanyProfileView(generics.CreateAPIView):
    serializer_class = CompanyProfileWithClassesSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                cp = CompanyProfile.objects.get(pk=pk)
            except:
                cp = CompanyProfile.objects.get(slug__iexact=pk)
        else:
            cp, _ = CompanyProfile.objects.get_or_create(
                user=request.user,
                defaults={'slug': uuid.uuid4()},
            )
        return Response(CompanyProfileWithClassesSerializer(cp).data)

    def post(self, request):
        data = request.data
        cp, _ = CompanyProfile.objects.get_or_create(
            user=request.user,
            defaults={'slug': uuid.uuid4()},
        )

        if data.get('profile'):
            cp.name = data['profile'].get('companyName')
            cp.title = data['profile'].get('title')
            cp.description = data['profile'].get('description')
            cp.replace_logo = data['profile'].get('replaceLogo', False)
            cp.reminder_day = data['profile'].get('reminderDay', False)
            cp.reminder_10min = data['profile'].get('reminder10Min', False)
            cp.reminder_renew = data['profile'].get('reminderRenew', False)
            cp.home_url = data['profile'].get('homeUrl')
            cp.member_center_url = data['profile'].get('memberCenterUrl')
            cp.about_us_url = data['profile'].get('aboutUsUrl')
            cp.slug = data['profile'].get('slug', uuid.uuid4())
            is_access_code_changed = cp.member_access_code != data['profile'].get('memberAccessCode')
            cp.member_access_code = data['profile'].get('memberAccessCode')
            if is_access_code_changed and cp.pk:
                try:
                    membership = Membership.objects.get(owner_user=request.user)
                    emails = [x.student.email for x in membership.students.all()]
                except Membership.DoesNotExist:
                    emails = []
                if emails:
                    for email in emails:
                        send_mail_reply_to(
                            '%s: Member Center Code' % cp.name,  # subject
                            'This is your access code to the member center: %s' % cp.member_access_code,  # body
                            settings.DEFAULT_FROM_EMAIL,
                            [email],
                            fail_silently=True,
                            reply_to=[cp.user.email],
                        )
        if data.get('avatar') and data['avatar']['uploadPhoto']['imageUrl']:
            imgstr = data['avatar']['uploadPhoto']['imageUrl']
            imgname = data['avatar']['uploadPhoto']['imageName']

            _, imgstr = imgstr.split(';base64,')
            name = '%s-%s-%s' % (cp.id, uuid.uuid1(), imgname)
            fdata = ContentFile(base64.b64decode(imgstr), name=name)
            cp.media = fdata
        if data.get('main_media') and data['main_media']['uploadPhoto']['imageUrl']:
            imgstr = data['main_media']['uploadPhoto']['imageUrl']
            imgname = data['main_media']['uploadPhoto']['imageName']

            _, imgstr = imgstr.split(';base64,')
            name = '%s-%s-%s' % (cp.id, uuid.uuid1(), imgname)
            fdata = ContentFile(base64.b64decode(imgstr), name=name)
            cp.main_media = fdata
        cp.save()
        cp.save_thumbnail()
        cp.save_main_thumbnail()

        status = True
        err = None
        if data.get('user'):
            email = data['user']['email']
            if request.user.username.lower() != email.lower():
                if User.objects.filter(username__iexact=email):
                    status = False
                    err = 'User with this email already exists'
                else:
                    request.user.email = email
                    request.user.username = email.lower()
                    request.user.save()
            request.user.phone = data['user'].get('phone')
            request.user.timezone = data['user'].get('timezone')
            request.user.first_name = data['user'].get('first_name')
            request.user.save()
            if data['user'].get('timezone_to_classes'):
                teachers = Teacher.objects.filter(user=request.user)
                Class.objects.filter(teacher__in=teachers).update(timezone=request.user.timezone)

        return Response({'success': status, 'err': err})


class DeactivateClass(APIView):
    def post(self, request):
        data = request.data
        if request.user.is_company:
            c = Class.objects.get(
                Q(pk=data.get('id')),
                Q(teacher__user=request.user) | Q(teacher__user__belongs_to=request.user.company.pk),
            )
        else:
            c = Class.objects.get(
                Q(pk=data.get('id')),
                Q(teacher__user=request.user),
            )
        if c.is_deactivated and not data.get('deactivate'):
            # enable payment
            c.is_paid_by_teacher = True
            if not c.activated_at or (datetime.now() - c.activated_at.replace(tzinfo=None) >= timedelta(days=30)):
                c.activated_at = datetime.now()
                if not request.user.is_free_member:
                    res = charge_for_class(c, request.user)
                    if not res['success']:
                        res['is_deactivated'] = c.is_deactivated
                        return Response(res)

        c.is_deactivated = data.get('deactivate', False)
        c.save()
        return Response({
            'is_deactivated': c.is_deactivated,
            'success': True,
        })


class MostRecentClassesView(APIView):
    def post(self, request):
        data = request.data
        today = datetime.now().strftime("%Y-%m-%d")
        c = Class.objects.filter(is_deactivated=False)
        c = c.filter(
            Q(until_date__isnull=True) |
            Q(until_date__gte=today)
        )
        if data.get('city') == 'all' and data.get('state') == 'all':
            pass
        elif data.get('city') == 'online':
            c = c.filter(class_type='online')
        else:
            if data.get('city'):
                c = c.filter(address_city=data['city'])
            if data.get('state'):
                c = c.filter(address_state=data['state'])
        cm = ClassMedia.objects.values('klass')
        c = c.filter(pk__in=cm)

        #categories = ['Language', 'Music', 'Career&Tech', 'Home&Repair', 'Arts&Crafts', 'Sports',]
        categories = [
            {'category': 'Career&Tech', 'count': 3},
            {'category': 'Sports', 'count': 6},
            {'category': 'Music', 'count': 3},
            {'category': 'Arts&Crafts', 'count': 3},
            {'category': 'Language', 'count': 3},
            {'category': 'Life skills', 'count': 1},
            {'category': 'Home&Repair', 'count': 1},
            {'category': 'Food', 'count': 1},
        ]
        res = []
        ids = {}
        for cat in categories:
            subcategories = SubCategory.objects.filter(category__name=cat['category']).values_list('pk', flat=True)
            cc = c.filter(subcategories__overlap=list(subcategories)).exclude(pk__in=list(ids.keys()))
            cc = cc.order_by('-created_at')
            removed = []
            added = []
            for cl in cc:
                #print(cat, i, cc.query, flush=True)

                if len(added) >= cat['count']:
                    break
                if cl.pk in ids:
                    continue
                if cl.teacher.id in added:
                    removed.append(dict({'category': cat['category']}, **ClassFullSerializer(cl).data))
                    continue
                res.append(dict({'category': cat['category']}, **ClassFullSerializer(cl).data))
                ids[cl.pk] = True
                added.append(cl.teacher.id)
            if len(added) < cat['count']:
                missing = cat['count']-len(added)
                for cl in removed:
                    if missing == 0:
                        break
                    res.append(cl)
                    missing -= 1

        return Response(res)


class ClassDetailsView(generics.RetrieveAPIView):
    def get(self, request, pk):
        c = Class.objects.get(pk=pk)
        resp = ClassFullSerializer(c).data
        if request.user.is_authenticated:
            order_ids = ClassLearner.objects.filter(
                klass=c,
                user=request.user
            ).values_list('pk', flat=True)
            resp['logged_in_user_orders'] = order_ids
        return Response(resp)

    def delete(self, request, pk):
        if request.user.is_company:
            c = Class.objects.get(
                Q(pk=pk),
                Q(teacher__user=request.user) | Q(teacher__user__belongs_to=request.user.company.pk),
            )
        else:
            c = Class.objects.get(
                pk=pk,
                teacher__user=request.user,
            )
        c.deleted_at = datetime.now(pytz.utc)
        c.save()
        return Response({'ok': True})


class AddSubCategoryView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def post(self, request):
        data = request.data
        category_id = data.get('category_id')
        subcategory_name = data.get('subcategory_name')

        sc = SubCategory.objects.filter(
            category_id=category_id,
            name=subcategory_name,
        )
        if sc:
            return Response({'id': sc[0].pk})
        sc = SubCategory(
            # user=request.user,
            category_id=category_id,
            name=subcategory_name,
        )
        if request.user.is_authenticated:
            sc.user = request.user

        sc.save()
        return Response({'id': sc.pk})


class ClassView(generics.ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def post(self, request):
        data = request.data
        orig_data = dict(request.data)
        if request.user.belongs_to:
            parent_company = CompanyProfile.objects.get(pk=request.user.belongs_to)
            owner_user = parent_company.user
        else:
            owner_user = request.user
        context = {'user': owner_user}
        data['subcategories'] = data.get('categories')
        if data['subcategories']:
            data['subcategories'] = list(set(data['subcategories']))
        data['is_private'] = data.get('teacherLessonType') == 'private'
        instance = None
        is_zoom_link_changed = False
        if data.get('teacherGroupClass'):
            dtg = data['teacherGroupClass']
            if dtg.get('id'):
                if request.user.is_company:
                    instance = Class.objects.get(
                        Q(pk=dtg['id']),
                        Q(teacher__user=request.user) | Q(teacher__user__belongs_to=request.user.company.pk)
                    )
                else:
                    instance = Class.objects.get(Q(pk=dtg['id']), Q(teacher__user=request.user) | Q(teacher__user=owner_user))

            data['name'] = dtg.get('groupClassName')
            if data['is_private']:
                data['name'] = dtg.get('privateClassName')
            data['group_description'] = dtg.get('groupClassDescription')
            data['experience'] = dtg.get('studentExperienceLevel')
            if data['experience'] == 'does not matter':
                data['experience'] = None
            data['students_bring'] = dtg.get('studentsBring')
            data['teacher_supplies'] = dtg.get('teacherSupply')
            data['what_else'] = dtg.get('studentsToKnow')
            data['class_type'] = dtg.get('whereTeach')
            # address
            data['address_google'] = dtg.get('teachingGooglePlace')
            data['address'] = dtg.get('teachingAddress')
            data['address_city'] = dtg.get('teachingCity')
            data['address_state'] = dtg.get('teachingState')
            data['address_zip'] = dtg.get('teachingZip')
            data['address_street'] = dtg.get('teachingStreet')
            data['address_country'] = dtg.get('teachingCountry')
            data['teaching_venue'] = dtg.get('teachingVenue')

            data['rate'] = dtg.get('lessonPricePerHour')
            if not data['rate']:
                data['rate'] = None

            data['drop_in_rate'] = dtg.get('dropInRate')
            if not data['drop_in_rate']:
                data['drop_in_rate'] = None

            data['group_lesson_length'] = dtg.get('lessonLengthGroup')
            data['private_lesson_length'] = dtg.get('lessonLengthPrivate')

            data['group_number_of_lessons'] = dtg.get('numOfLessonsGroup')
            data['private_number_of_lessons'] = dtg.get('numOfLessonsPrivate')

            data['schedule_dates'] = dtg.get('scheduleDates')
            data['schedule_from'] = dtg.get('scheduleFrom')
            data['schedule_to'] = dtg.get('scheduleTo')
            data['instant_booking'] = dtg.get('allowStudentsBookInstantly')
            data['weekdays_schedule'] = dtg.get('weekdaysScheduled')

            data['day_select_type'] = dtg.get('daySelectType')
            data['flexible_dates'] = dtg.get('flexibleDates', False)
            data['until_date'] = dtg.get('untilDate')
            data['start_date'] = dtg.get('startDate')
            data['groupClassSummary'] = dtg.get('groupClassSummary')
            if dtg.get('maxSize'):
                data['maxSize'] = int(dtg['maxSize'])
            data['lat'] = dtg.get('lat')
            data['lng'] = dtg.get('lng')
            data['point'] = Point(x=data['lng'], y=data['lat'], srid=4326)
            data['show_email'] = dtg.get('showEmail')
            data['show_phone'] = dtg.get('showPhone')
            if dtg.get('showPhoneRule'):
                data['show_phone_rule'] = dtg.get('showPhoneRule')
            data['is_premium_community'] = dtg.get('isPremiumCommunity', False)
            data['zoom_link'] = dtg.get('zoomLink')

            is_zoom_link_changed = instance and instance.zoom_link != data['zoom_link']

            try:
                tz_url = "https://maps.googleapis.com/maps/api/timezone/json?location=%s,%s&timestamp=1458000000&key=%s" % (
                    data['lat'],
                    data['lng'],
                    os.environ['GOOGLE_MAPS_API_KEY'],
                )
                with urllib.request.urlopen(tz_url) as url:
                    x = json.loads(url.read().decode())
                    data['timezone'] = x['timeZoneId']
            except:
                if request.user.timezone:
                    data['timezone'] = request.user.timezone
            if not data['timezone']:
                data['timezone'] = 'America/Mazatlan'
            # data['timezone'] = dtg.get('timezone', 'America/New_York')

            if dtg.get('scheduleDatesExcluded'):
                schedule_excluded = []
                for x in dtg['scheduleDatesExcluded'].values():
                    schedule_excluded += x
                data['schedule_excluded'] = schedule_excluded
            data['standard_packages'] = dtg.get('standardPackages')
            data['custom_packages'] = dtg.get('customPackages')
            data['group_package_type'] = dtg.get('groupPackageType')

            data['teaching_country'] = dtg.get('teachingCountry')
            data['private_class_website'] = dtg.get('privateClassWebsite')
            data['private_className'] = dtg.get('privateClassName')
            data['location_other'] = dtg.get('locationOther')
            data['currency'] = dtg.get('currency')

            data['can_book'] = dtg.get('canBook', True)
            data['can_book_url'] = dtg.get('canBookUrl')
            data['can_pay'] = dtg.get('canPay', True)
            data['is_price_hidden'] = dtg.get('isPriceHidden', False)

        data['class_data'] = orig_data

        if data.get('profile') and data['profile'].get('id'):
            if request.user.is_company:
                teacher = Teacher.objects.get(
                    Q(user=request.user) | Q(user__belongs_to=request.user.company.pk),
                    Q(pk=data['profile']['id']),
                )
            else:
                teacher = Teacher.objects.get(
                    Q(user=request.user) | Q(user=owner_user),
                    Q(pk=data['profile']['id']),
                )
        else:
            teacher = Teacher.objects.get(user=request.user)
        data['teacher'] = teacher.pk

        pay_id = None
        if not instance:
            data['created_at'] = datetime.now(pytz.utc)
            klass = None
            draft = DraftClass.objects.filter(user=request.user)
            if draft:
                klass = draft[0]
                if not owner_user.is_free_member:
                    pay_resp = charge_for_class(klass, owner_user, is_draft=True)
                    if pay_resp['success']:
                        pay_id = pay_resp['pay_id']
                    else:
                        # return Response(pay_resp)
                        pass

        if 'is_premium_community' not in data:
            data['is_premium_community'] = False
        class_data = ClassWriteSerializer(instance=instance, data=data, context=context)
        class_data.is_valid(raise_exception=True)
        klass = class_data.save()
        if not instance and pay_id is None and not owner_user.is_free_member:
            klass.activated_at = None
            klass.is_deactivated = True
            klass.save()
        # class saved - remove draft
        DraftClass.objects.filter(user=request.user).delete()

        # notification
        if not instance:
            if pay_id:
                update_payment(pay_id, klass.pk)
            send_mail(
                'New class added',  # subject
                'New class added %s/class/%s' % (settings.FULL_URL, klass.pk),  # body
                settings.DEFAULT_FROM_EMAIL,
                ['alisacromer@gmail.com'],
                fail_silently=True,
            )

        if data.get('profile'):
            klass.teacher.description = data['profile'].get('description')
            klass.teacher.areas_of_specialty = data['profile'].get('areasOfSpeciality')
            klass.save()

        # save global packages
        if data['standard_packages']:
            for x in data['standard_packages']:
                if x.get('isGlobalPackage'):
                    gp_data = {
                        'teacher': klass.teacher.pk,
                        'packages': x,
                    }
                    gp = GlobalPackageSerializer(data=gp_data)
                    gp.is_valid(raise_exception=True)
                    gp.save()

        if instance:
            # TODO: process schedule update (remove enrollments that do not match new schedule)
            print("check schedule")
            def get_mismatch(list_old, list_new, hasher_fn):
                dict_old = dict.fromkeys(map(hasher_fn, list_old), True)
                dict_new = dict.fromkeys(map(hasher_fn, list_new), True)
                missing_old = []
                missing_new = []
                for item in list_old:
                    if not dict_new.get(hasher_fn(item), False):
                        missing_old.append(item)
                for item in list_new:
                    if not dict_old.get(hasher_fn(item), False):
                        missing_new.append(item)
                return (missing_old, missing_new)

            if instance.day_select_type == 'monthly':
                # check if new schedule_dates doesn't match
                mapper = lambda x: "%s|%s|%s" % (x['date'], x['start'], x['end'])
                (missing_old, missing_new) = get_mismatch(instance.schedule_dates, data['schedule_dates'], mapper)
                if len(missing_old) or len(missing_new):
                    print('mismatch', missing_old, missing_new)
                    enrollments = GroupEnroll.objects.filter(
                        order__klass=instance,
                    )
                    if instance.flexible_dates:
                        # flexible dates, check every enrollemnt and remove that has no match
                        missing_old_dict = dict.fromkeys(map(mapper, missing_old), True)
                        for enr in enrollments:
                            if "%s|%s|%s" % (enr.date, enr.time_from, enr.time_to) in missing_old_dict:
                                # remove corresponding enrollment
                                enr.status = "rejected"
                                enr.save()
                    else:
                        # fixed dates, just remove old enrollments and create new for actual dates
                        missing_old_dict = dict.fromkeys(map(mapper, missing_old), True)
                        missing_new_dict = dict.fromkeys(map(mapper, missing_new), True)
                        affected_orders = set()
                        for enr in enrollments:
                            if "%s|%s|%s" % (enr.date, enr.time_from, enr.time_to) in missing_new_dict or "%s|%s|%s" % (enr.date, enr.time_from, enr.time_to) in missing_old_dict:
                                affected_orders.add(enr.order)
                        # delete enrollments from affectd orders
                        GroupEnroll.objects.filter(
                            order__in=affected_orders,
                        ).delete()
                        # create enrollments for all new dates
                        for enr in enrollments:
                            for new_date in data['schedule_dates']:
                                class_tz = pytz.timezone(enr.order.klass.timezone)
                                x = datetime.strptime('%s %s' % (new_date['date'], new_date['start']), '%Y-%m-%d %H:%M')
                                x = class_tz.localize(x)

                                enr_data = {
                                    'order': enr.order.pk,
                                    'date': new_date['date'],
                                    'time_from': new_date['start'],
                                    'time_to': new_date['end'],
                                    'time_from_gmt': x,
                                }
                                ges = GroupEnrollSerializer(data=enr_data)
                                ges.is_valid(raise_exception=True)
                                ges.save()

        if data.get('teacherGroupClass'):
            if dtg.get('supportFiles'):
                if instance:
                    # remove deleted images
                    all_ids = [x.get('id') for x in dtg['supportFiles'] if x.get('id')]
                    ClassMedia.objects.filter(klass=instance).exclude(pk__in=all_ids).delete()
                for file in dtg['supportFiles']:
                    if not file.get('id'):
                        cm_data = {'klass': klass.pk, 'class_media': file['imageUrl']}
                        cms = ClassMediaSerializer(data=cm_data)
                        cms.is_valid(raise_exception=True)
                        cm_obj = cms.save()
                        # save thumbnail
                        cm_obj.save_thumbnail()
        bm = BoostMembership.objects.filter(
            user=owner_user,
            valid=True,
        ).last()

        if is_zoom_link_changed:
            # send email to enrollers
            cl = ClassLearner.objects.filter(
                klass=instance,
            )
            for c in cl:
                dates = []
                if not klass.is_private:
                    today = datetime.now().strftime("%Y-%m-%d")
                    gr = GroupEnroll.objects.filter(
                        order=c,
                        date__gte=today,
                    ).first()
                    if gr:
                        d_str = format_date_time_from_to(gr.date, gr.time_from, gr.time_to)
                        dates.append(d_str)
                dates_tz = klass.get_timezone()
                email_body = """Hi %s, 

Confirmed! You are booked for "%s with %s" on:
%s
Time zone: %s
%s

Sync to your personal calendar here %s
Keep track on your own dashboard here: %s

Look forward to working with you!

See you soon! 

All the best, 

%s
%s
%s
""" % (
    c.user.first_name,
    klass.name,
    klass.teacher.first_name,
    "\n".join(dates),
    dates_tz,
    'Please use this link to join the session: ' + data.get('zoom_link'),
    settings.FULL_URL + '/dashboard/learn/calendar',
    settings.FULL_URL + '/dashboard/learn/classes',
    klass.teacher.first_name,
    klass.teacher.phone or klass.teacher.user.phone,
    klass.teacher.email or klass.teacher.user.email,
)
                if len(dates):
                    send_mail(
                        'Zoom link for class %s has changed' % data['name'],  # subject
                        email_body,  # body
                        settings.DEFAULT_FROM_EMAIL,
                        [c.user.email],
                        fail_silently=True,
                    )
        return Response({
            'success': True,
            'id': klass.pk,
            'current_option': BoostMembershipSerializer(bm).data if bm else None,
            'isBankAccount': owner_user.has_external_account,
            'isFirstClass': True if len(Class.objects.filter(teacher=klass.teacher)) == 1 else False,
            'isFreeMember': owner_user.is_free_member,
        })


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class SubCategoryViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        classes = Class.objects.all()
        today = datetime.now().strftime("%Y-%m-%d")
        classes = classes.filter(
            Q(until_date='') |
            Q(until_date__isnull=True) |
            Q(until_date__gte=today)
        )
        classes = classes.exclude(Q(flexible_dates=False) & Q(is_private=False) & Q(start_date__lte=today) & Q(drop_in_rate__isnull=True))
        subcategories = classes.annotate(
            arr_els=Func(F('subcategories'), function='unnest')
        ).values_list('arr_els', flat=True).distinct()

        queryset = SubCategory.objects.filter(pk__in=subcategories)
        return queryset

    serializer_class = SubCategorySerializer
    pagination_class = None


class HandShakeView(APIView):
    def get(self, request, format=None):
        data = {
            'csrftoken': csrf.get_token(request),
            'is_authenticated': request.user.is_authenticated,
        }
        return Response(data)


class InitView(APIView):
    def get(self, request, format=None):
        user_data = None
        last_class = None
        teacher = None
        learner_needs = None
        has_order = False
        last_lesson = None
        if request.user.is_authenticated:
            user_data = UserSerializer(request.user).data
            teachers = Teacher.objects.filter(user=request.user)
            cl = ClassLearner.objects.filter(user=request.user).last()
            if cl:
                learner_needs = cl.learnerNeeds
                has_order = True
                last_lesson = ClassLearnerSerializer(cl).data
                last_lesson['data']['class']['enrolled'] = None
                last_lesson['data']['class']['orders'] = None
            if teachers:
                classes = Class.objects.filter(teacher=teachers[0]).last()
                last_class = ClassSerializer(classes).data
                teacher = TeacherSerializer(teachers[0]).data
        data = {
            'user': user_data,
            'teacher': teacher,
            'last_class': last_class,
            'csrftoken': csrf.get_token(request),
            'learner_needs': learner_needs,
            'has_order': has_order,
            'last_lesson': last_lesson,
        }
        return Response(data)


class CityView(APIView):
    def get(self, request):
        today = datetime.now().strftime("%Y-%m-%d")
        classes = Class.objects.filter(address_city__gt='')
        classes = classes.filter(
            Q(until_date__isnull=True) |
            Q(until_date__gte=today)
        )

        classes = classes.filter(start_date__lte=today)

        cities = classes.values('address_city', 'address_state').distinct()
        return Response(cities)


class ZipView(APIView):
    def get(self, request):
        today = datetime.now().strftime("%Y-%m-%d")
        classes = Class.objects.filter(address_zip__gt='')
        classes = classes.filter(
            Q(until_date__isnull=True) |
            Q(until_date__gte=today)
        )

        classes = classes.filter(start_date__lte=today)
        zips = classes.values_list('address_zip', flat=True).distinct()
        return Response(zips)


class SearchClassView(APIView, MyPaginationMixin):
    pagination_class = LimitOffsetPagination
    serializer_class = ClassFullSerializer

    def post(self, request):
        classes = Class.objects.filter(is_deactivated=False)
        data = request.data

        radius = 80500  # 50 miles in meters
        lat, lng = None, None

        limit = data.get('limit')

        if data.get('classId'):
            serializer = self.serializer_class(classes.filter(pk=data.get('classId')), many=True)
            return Response(serializer.data)

        if data.get('teacher'):
            serializer = self.serializer_class(classes.filter(teacher=data.get('teacher')), many=True)
            return Response(serializer.data)

        try:
            if data.get('city') == 'all' and data.get('state') == 'all':
                pass
            elif data.get('city'):
                addr = "%s %s" % (
                    data.get('city'),
                    data.get('state'),
                )
                f = {
                    'key' : os.environ['GOOGLE_MAPS_API_KEY'],
                    'address' : addr,
                }

                api_url = "https://maps.googleapis.com/maps/api/geocode/json?%s" % urllib.parse.urlencode(f)

                with urllib.request.urlopen(api_url) as url:
                    x = json.loads(url.read().decode())
                    lat = x['results'][0]['geometry']['location']['lat']
                    lng = x['results'][0]['geometry']['location']['lng']
        except:
            pass

        if data.get('isMaster'):
            classes = classes.filter(is_master=True)
        if data.get('lessonType'):
            is_private = data['lessonType'] == 'private'
            classes = classes.filter(is_private=is_private)
        # if data.get('categoriesSelected'):
        #     subcategories = data['categoriesSelected'].values()
        #     classes = classes.filter(user_subcategory__in=subcategories)
        if data.get('subcategory'):
            try:
                subcategory_id = int(data.get('subcategory'))
                subcategories = [subcategory_id]
                classes = classes.filter(subcategories__overlap=subcategories)
            except:
                pass
        elif data.get('category') and int(data.get('category')):
            category_id = int(data.get('category'))
            subcategories = list(SubCategory.objects.filter(category=category_id).values_list('pk', flat=True))
            classes = classes.filter(subcategories__overlap=subcategories)

        is_online = False
        if data.get('city'):
            if type(data['city']) == str and data['city'] == 'online':
                is_online = True
                classes = classes.filter(class_type='online')
            elif lat:
                pnt = GEOSGeometry('POINT(%s %s)' % (lng, lat), srid=4326)
                desired_radius = {'m': radius}
                classes = classes.filter(
                    point__distance_lte=(pnt, D(**desired_radius)))
            elif data['city'] == 'all' and data['state'] == 'all':
                pass
            else:
                classes = classes.filter(
                    address_city=data['city'],
                    address_state=data['state'],
                )
        if not is_online and data.get('zip'):
            classes = classes.filter(address_zip=data['zip'])

        if data.get('venue'):
            classes = classes.filter(teaching_venue=data['venue'])

        today = datetime.now().strftime("%Y-%m-%d")
        if data.get('timeInterval'):
            from_date = datetime.strptime(data['timeInterval']['from'], '%Y-%m-%d')
            to_date = datetime.strptime(data['timeInterval']['to'], '%Y-%m-%d')
            assert to_date > from_date

            classes = classes.filter(
                Q(until_date__isnull=True) |
                Q(until_date__gte=from_date)
            )

            # classes = classes.filter(start_date__lte=to_date)
            classes = classes.exclude(Q(flexible_dates=False) & Q(is_private=False) & Q(start_date__lte=today) & Q(drop_in_rate__isnull=True))

            dates = []
            d = from_date
            while d <= to_date:
                dates.append(d.strftime("%Y-%m-%d"))
                d = d + timedelta(days=1)
            res = []
            for c in classes:
                include = False
                # selected dates
                if c.schedule_dates:
                    # daily
                    for d in dates:
                        if d in [x['date'] for x in c.schedule_dates]:
                            include = True
                            break
                # weekdays
                if c.weekdays_schedule:
                    d = from_date
                    while d <= to_date:
                        wd = d.isoweekday() % 7
                        rules = [x for x in c.weekdays_schedule if x.get('weekday') == wd]
                        day_x = d.strftime("%Y-%m-%d")
                        if rules and (not c.schedule_excluded or day_x not in c.schedule_excluded):
                            include = True
                            break
                        d = d + timedelta(days=1)

                if include:
                    res.append(c)
            classes = res
        else:

            classes = classes.filter(
                Q(until_date__isnull=True) |
                Q(until_date__gte=today)
            )

            classes = classes.exclude(
                Q(flexible_dates=False) & Q(is_private=False) & Q(start_date__lte=today) & Q(drop_in_rate__isnull=True))

        classes = classes.order_by('-id')
        page = None
        if data.get('paginated'):
            page = self.paginate_queryset(classes)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(classes, many=True)
        return Response(serializer.data)


class LearnerView(generics.ListAPIView):
    queryset = ClassLearner.objects.all()
    serializer_class = ClassLearnerSerializer

    def post(self, request):
        data = request.data
        data['klass'] = data.pop('classId')

        cl = ClassLearnerSerializer(data=data)
        cl.is_valid(raise_exception=True)
        c = cl.save()

        send_text(
            "%s enrolled in class %s" % (
                c.email,
                c.klass,
            ),
            settings.TEXT_NOTIFICATIONS
        )

        return Response({'success': True})


class StripeDeleteCardView(generics.ListAPIView):

    def post(self, request, pk):
        stripe.api_key = os.environ['STRIPE_SECRET_KEY']
        uc = UserCard.objects.filter(
            user=request.user,
        )
        if uc and uc[0].customer_id:
            stripe.Customer.delete_source(
                uc[0].customer_id,
                pk
            )

        return Response({'success': True})


class StripeDefaultCardView(generics.ListAPIView):

    def post(self, request, pk):
        stripe.api_key = os.environ['STRIPE_SECRET_KEY']
        uc = UserCard.objects.filter(
            user=request.user,
        )
        if uc:
            stripe.Customer.modify(
                uc[0].customer_id,
                default_source=pk
            )

        return Response({'success': True})


class EnrollNoPayClassView(generics.ListAPIView):
    def post(self, request):
        data = request.data
        klass = data.get('class')

        # cost in cents
        cost = float(data.get('cost'))
        cost = int(cost*100)
        if data.get('package'):
            desc = '%s lessons for $%s' % (
                data['package'].get('numberOfLessons'),
                data['package'].get('perLesson'),
            )
        else:
            desc = 'Teachbeach private lesson'
        c = Class.objects.get(pk=klass.get('id'))

        checkout = {
            'klass': klass.get('id'),
            'alerts': data.get('alerts', False),
            'data': data,
            'user': request.user.pk,
            'amount': cost/100,
            'amount_full': cost/100,
            'num_lessons': data['package'].get('numberOfLessons', 1),
            'no_pay': True,
            #'learnerNeeds': data.get('learnerNeeds'),
        }

        cl = ClassLearnerSerializer(data=checkout)
        cl.is_valid(raise_exception=True)
        c = cl.save()

        # Sale notification
        # link = settings.FULL_URL + '/dashboard/teach/classes'  # % c.klass.pk
        # text = 'TeachBeach: It´s sunny! (%s has enrolled) See more: %s' % (
        #     c.user,
        #     link,
        # )
        # if c.klass.teacher.user.phone:
        #     send_text(
        #         text,
        #         c.klass.teacher.user.phone
        #     )
        # send_mail(
        #     text,  # subject
        #     text,  # body
        #     settings.DEFAULT_FROM_EMAIL,
        #     [c.klass.teacher.user.email],
        #     fail_silently=True,
        # )

        return Response({'success': True, 'order_id': c.id})


class StripeBuyMembershipView(generics.ListAPIView):

    def post(self, request):
        stripe.api_key = os.environ['STRIPE_SECRET_KEY']
        data = request.data
        membership_id = data.get('membership_id')
        period = data.get('period')
        token = data.get('token')
        card_id = data.get('card_id')
        uc, created = UserCard.objects.get_or_create(user=request.user)
        membership = Membership.objects.get(pk=membership_id)
        if not period:
            return Response({'success': False, 'error_message': "Please choose an option"})
        try:
            student_membership = MembershipStudent.objects.create(
                student=request.user,
                membership=membership,
                currency=membership.currency,
                weekly_rate=membership.weekly_rate,
                monthly_rate=membership.monthly_rate,
                yearly_rate=membership.yearly_rate,
                period=period,
                amount=0,
                amount_full=0,
            )
        except Exception as e:
            return Response({'success': False, 'error_message': "Membership for this user already exists"})
        interval = 'month'
        if period == 'weekly':
            interval = 'week'
        if period == 'yearly':
            interval = 'year'
        plan = stripe.Plan.create(
            amount=int(membership.monthly_rate * 100),
            currency=membership.currency,
            interval=interval,
            interval_count=1,
            product={"name": "Teachbeach membership"},
        )
        try:
            subs = stripe.Subscription.create(
                customer=uc.customer_id,
                items=[{"plan": plan.id}],
                default_payment_method=card_id,
            )
            student_membership.session_id = subs['id']
            student_membership.status = subs['status']
            student_membership.current_period_start = subs['current_period_start']
            student_membership.current_period_end = subs['current_period_end']
            student_membership.save()
        except Exception as e:
            student_membership.delete()
            return Response({'success': False, 'error_message': e.user_message, "membership_id": membership_id})
        return Response({'success': True, 'student_membership': MembershipStudentSerializer(student_membership).data, "status": subs['status']})


class StripeCancelMembershipView(generics.ListAPIView):

    def post(self, request):
        stripe.api_key = os.environ['STRIPE_SECRET_KEY']
        data = request.data
        student_membership_id = data.get('student_membership_id')
        student_membership = MembershipStudent.objects.get(pk=student_membership_id)
        try:
            res = stripe.Subscription.delete(
              student_membership.session_id,
            )
            student_membership.deactivated_at = datetime.now(pytz.utc)
            student_membership.status = 'canceled'
            student_membership.end_at = datetime.utcfromtimestamp(student_membership.current_period_end)
            student_membership.save()
        except Exception as e:
            return Response({'success': False, 'error_message': e.user_message})
        return Response({'success': True, 'student_membership': MembershipStudentSerializer(student_membership).data})


class StripeAddCardView(generics.ListAPIView):

    def create_order_plan(self, order, customer_id, card_id):
        plan = stripe.Plan.create(
            amount=int(order.amount_full*100),
            currency="usd",
            interval=order.interval,
            interval_count=order.interval_count,
            product={"name": "Teachbeach class subscription"},
        )

        try:
            subs = stripe.Subscription.create(
                customer=customer_id,
                items=[{"plan": plan.id}],
                default_payment_method=card_id,
                cancel_at=int(time.mktime(order.end_at.timetuple())),
            )
            status = subs['status']
            stripe_id = subs['id']
        except Exception as e:
            order.delete()
            return Response({'success': False, 'error_message': e.user_message, 'order_id': order.id})
        order.status = status
        order.session_id = stripe_id
        order.num_lessons_per_interval = order.num_lessons
        order.current_period_start = subs['current_period_start']
        order.current_period_end = subs['current_period_end']
        order.save()
        res = {
            'success': status == 'active',
            'charge_id': stripe_id,
            'order_id': order.id,
            'status': status,
        }
        if not res['success']:
            res['error_message'] = f'{status}. Check your card'
        return Response(res)

    def post(self, request):
        stripe.api_key = os.environ['STRIPE_SECRET_KEY']

        data = request.data
        klass = data.get('class')
        token = data.get('token')
        card_id = data.get('card_id')

        uc, created = UserCard.objects.get_or_create(user=request.user)

        if token and card_id == 'new_card' and token.get('card'):
            try:
                if not uc.customer_id:
                    customer = stripe.Customer.create(
                        source=token['id'],
                        email=request.user.email,
                    )
                    card_id = customer['default_source']
                    uc.customer_id = customer.id
                    uc.save()
                else:
                    card = stripe.Customer.create_source(
                        uc.customer_id,
                        source=token['id']
                    )
                    card_id = card['id']
                stripe.Customer.modify(
                    uc.customer_id,
                    default_source=card_id
                )
            except stripe.error.CardError as e:
                err_message = e.user_message
                err = e.json_body.get('error', {})
                err_code = err.get('code')
                decline_code = err.get('decline_code')

                ce = CardError(
                    user=request.user,
                    json=e.json_body,
                    req=e.request_id,
                )
                ce.save()
                return Response({
                    'success': False,
                    'error_message': err_message,
                    'code': err_code,
                    'decline_code': decline_code,
                })

        if data.get('no_pay'):
            if card_id == 'new_card' and (not token or not token.get('card')):
                return Response({'success': False, 'error_message': 'No token'})
            return Response({'success': True})

        class_instance = Class.objects.get(pk=klass.get('id'))
        try:
            membership = MembershipStudent.objects.get(
                student=request.user,
                membership__owner_user=class_instance.teacher.user,
                is_active=True,
            )
        except MembershipStudent.DoesNotExist:
            membership = None

        # cost in cents
        package = data.get('package')
        cost = None
        if package.get('type') == 'limitedSubscription':
            cost = float(package.get('memberPricePerInterval')) if membership else float(package.get('pricePerInterval'))
        if class_instance.is_private and package.get('isSubscription'):
            cost = float(package.get('memberTotalPrice') if membership else package.get('rateBilled'))
        base_price = package.get('memberTotalPrice') if membership else package.get('totalPrice')
        if not cost:
            if class_instance.is_private:
                cost = float(base_price * (data.get('persons') or 1 if package.get('isPricePerPerson') else 1))
            else:
                cost = float(base_price * (data.get('persons') or 1))
        service_fee = float(data.get('serviceFee'))
        assert service_fee >= 0
        cost = int(cost*100)
        service_fee = int(service_fee*100)
        c = Class.objects.get(pk=klass.get('id'))

        if not c.is_private and data.get('package'):
            desc = '%s lessons for $%s' % (
                data['package'].get('numberOfLessons'),
                data['package'].get('perLesson'),
            )
        else:
            desc = 'Teachbeach private lesson'

        checkout = {
            'klass': klass.get('id'),
            'alerts': data.get('alerts', False),
            'data': data,
            'user': request.user.pk,
            'amount': cost/100,
            'amount_full': (cost + service_fee)/100,
            #'learnerNeeds': data.get('learnerNeeds', None),
            'is_subscription': data['package'].get('isSubscription', False) or data['package'].get('type', '') == 'limitedSubscription',
        }
        checkout['num_lessons'] = data['package'].get('numberOfLessons', 1)
        if data['package'].get('isSubscription', False):
            interval, interval_count = data['package']['period'].split('|')
            interval_count = int(interval_count)
            assert interval in ('day', 'week', 'month', 'year')
            checkout['interval'] = interval
            checkout['interval_count'] = interval_count
            checkout['num_lessons'] = data['package']['classesPerInterval']
            noi = data['package']['numberOfIntervals']
            dur_in = interval_count*noi
            if interval == 'day':
                duration = timedelta(days=dur_in)
            if interval == 'week':
                duration = timedelta(weeks=dur_in)
            if interval == 'month':
                duration = monthdelta(dur_in)
            if interval == 'year':
                duration = monthdelta(dur_in*12)
            checkout['end_at'] = datetime.now() + duration

        if data['package'].get('type', '') == 'limitedSubscription':
            interval = data['package']['interval']
            interval_count = 1
            assert interval in ('day', 'week', 'month', 'year')
            checkout['interval'] = interval
            checkout['interval_count'] = interval_count
            checkout['num_lessons'] = 999
            noi = int(data['package']['numberOfIntervals'])
            dur_in = interval_count*noi
            if interval == 'day':
                duration = timedelta(days=dur_in)
            if interval == 'week':
                duration = timedelta(weeks=dur_in)
            if interval == 'month':
                duration = monthdelta(dur_in)
            if interval == 'year':
                duration = monthdelta(dur_in*12)
            checkout['end_at'] = datetime.now() + duration

        cl = ClassLearnerSerializer(data=checkout)
        cl.is_valid(raise_exception=True)
        cl_obj = cl.save()

        if checkout['is_subscription']:
            return self.create_order_plan(cl_obj, uc.customer_id, card_id)

        charge = None
        try:
            charge = stripe.Charge.create(
                amount=cost + service_fee,
                currency='usd',
                description=desc,
                # source=token['id'],
                customer=uc.customer_id,
                source=card_id,
                # application_fee_amount=service_fee,
            )
        except stripe.error.CardError as e:
            cl_obj.delete()
            return Response({'success': False, 'error_message': e.user_message, 'order_id': cl_obj.id})

        cl_obj.session_id = charge['id']
        cl_obj.save()

        # # Sale notification
        # link = settings.FULL_URL + '/dashboard/teach/classes'  # % c.klass.pk
        # text = 'TeachBeach: It´s sunny! (%s has enrolled) See more: %s' % (
        #     c.user,
        #     link,
        # )
        # if c.klass.teacher.user.phone:
        #     send_text(
        #         text,
        #         c.klass.teacher.user.phone
        #     )
        send_mail(
            'Teachbeach: New order',  # subject
            f'{cl_obj.user.email} has bought class https://www.teachbeach.com/class/{cl_obj.klass.pk}',  # body
            settings.DEFAULT_FROM_EMAIL,
            ['alisacromer@teachbeach.com'],
            fail_silently=True,
        )

        # # notification to student
        # link = settings.FULL_URL + '/dashboard/learn/classes'
        # text = 'Thanks for your payment! Please schedule a time for your classes with %s: %s  ' % (
        #     c.teacher.first_name,
        #     link,
        # )
        # send_mail(
        #     'Teachbeach: New order',  # subject
        #     text,  # body
        #     settings.DEFAULT_FROM_EMAIL,
        #     [request.user.email, ],
        #     fail_silently=True,
        # )
        # if request.user.phone:
        #     send_text(
        #         text,
        #         request.user.phone
        #     )


        return Response({'success': True, 'charge_id': charge['id'], 'order_id': cl_obj.id})


class LearnerClassPackageView(generics.RetrieveAPIView):
    queryset = ''

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=401)
        res = []
        cl = ClassLearner.objects.filter(
            user=request.user,
            klass=pk,
        )
        for c in cl:
            if c.data.get('package'):
                res.append(c.data.get('package'))
        return Response(res)


class NewsletterView(generics.CreateAPIView):
    def post(self, request):
        data = request.data
        newsletter = NewsletterSerializer(data=data)
        newsletter.is_valid(raise_exception=True)
        nl = newsletter.save()
        # send email
        email_list = [
            'alisacromer@gmail.com',
            'Partha pratim Deb <debparthapratim0@gmail.com>',
        ]
        text = '%s in %s. Teacher: %s Learner: %s' % (
            nl.email, nl.city, nl.is_teacher, nl.is_learner,
        )

        send_mail(
            'newsletter signup: %s' % nl.email,  # subject
            text,  # body
            settings.DEFAULT_FROM_EMAIL,
            email_list,
            fail_silently=True,
        )

        res = {
            'status': True,
        }
        return Response(res)


class OrderRefundView(generics.CreateAPIView):

    def post(self, request, pk):
        c = ClassLearner.objects.filter(
            Q(klass__teacher__user=request.user)
        ).get(pk=pk)

        status = 'No succeeded payment yet'
        if not c.no_pay and c.status == 'succeeded' and c.session_id:
            stripe.api_key = os.environ['STRIPE_SECRET_KEY']

            s = stripe.Charge.retrieve(c.session_id)

            refund = stripe.Refund.create(
                charge=c.session_id,
            )

            c.status = 'refund'
            c.save()
            status = refund.status


        res = {
            'status': status,
        }
        return Response(res)


class OrderView(generics.RetrieveAPIView):
    def get(self, request, pk):
        c = ClassLearner.objects.filter(
            Q(user=request.user) | Q(klass__teacher__user=request.user)
        ).get(pk=pk)

        if not c.no_pay and c.status not in ('succeeded', 'refund') and c.session_id:
            stripe.api_key = os.environ['STRIPE_SECRET_KEY']

            if c.is_subscription:
                c.update_subsciption_data()
            else:
                s = stripe.Charge.retrieve(c.session_id)
                c.status = s['status']
                c.save()

        EnrModel = GroupEnroll
        if c.klass.is_private:
            EnrModel = PrivateEnroll
        enr = EnrModel.objects.filter(
            order=c,
        )
        res = {
            'data': ClassLearnerSerializer(c).data['data'],
            'class_enrolled': ClassFullSerializer(c.klass).data['enrolled'],
            'order_enrolled': GroupEnrollSerializer(enr, many=True).data,
            'status': c.status,
            'current_period_start': c.current_period_start,
            'current_period_end': c.current_period_end,
            'end_at': int(time.mktime(c.end_at.timetuple())) if c.end_at else None,
            'num_lessons': c.num_lessons,
        }
        return Response(res)

    def post(self, request, pk):
        try:
            if request.user.is_company:
                order = ClassLearner.objects.get(
                    Q(pk=pk),
                    Q(klass__teacher__user=request.user) | Q(klass__teacher__user__belongs_to=request.user.company.pk)
                )
            else:
                order = ClassLearner.objects.get(
                    pk=pk,
                    klass__teacher__user=request.user,
                )
        except ClassLearner.DoesNotExist:
            return Response({'status': False})
        data = request.data.get('data')
        if data:
            if data['isRemovedNotification']:
                order.data['isRemovedNotification'] = data['isRemovedNotification']
        order.save()
        return Response({'status': True})


class EnrFromSecretView(generics.RetrieveAPIView):
    def get(self, request, key):
        pe = PrivateEnroll.objects.filter(secret=key)
        if not pe:
            return Response({'status': False})

        # request.user = pe[0].order.klass.teacher.user
        login(request, pe[0].order.klass.teacher.user)
        # copy-paste from TeacherClasses
        teachers = Teacher.objects.filter(user=request.user)
        if not teachers:
            teacher = Teacher(user=request.user)
            teacher.save()
            teachers = Teacher.objects.filter(user=request.user)

        today = datetime.now().strftime("%Y-%m-%d")

        pr = PrivateEnroll.objects.filter(
            order__klass__teacher__in=teachers,
            date__gte=today,
        )
        gr = GroupEnroll.objects.filter(
            order__klass__teacher__in=teachers,
            date__gte=today,
        )

        classes = Class.objects.filter(teacher__in=teachers)

        amount = ClassLearner.objects.filter(
            klass__teacher__user=request.user,
            no_pay=False,
            status='succeeded',
            paid_status=1,
        ).aggregate(sum=Sum('amount'))
        bank_message = ''
        if amount['sum'] and not request.user.has_external_account:
            bank_message = 'You have $%s waiting ' % (amount['sum'] or 0)

        bm = BoostMembership.objects.filter(user=request.user, valid=True).last()
        boosted = classes.filter(is_boosted=True).count()

        res = {
            'private_enroll':  PrivateEnrollDetailsSerializer(pr, many=True).data,
            'group_enroll':  GroupEnrollDetailsSerializer(gr, many=True).data,
            'classes': ClassShortSerializer(classes, many=True).data,
            'bank_message': bank_message,
            'boost_classes_num': None,
        }
        if bm:
            res['boost_classes_num'] = bm.num_classes - boosted

        return Response(res)


class PrivateEnrollView(generics.ListAPIView):
    def post(self, request):
        data = request.data
        order = ClassLearner.objects.get(
            pk=data.get('orderId'),
            user=request.user
        )
        if order.is_subscription and order.status != 'active':
            return Response({
                'status': False,
                'message': order.status,
            })
        is_first_lesson = len(ClassLearner.objects.filter(user=request.user)) == 1 and order.reserved_lessons == 0
        class_tz = pytz.timezone(order.klass.timezone)

        keep_pe = []
        for item in data.get('dates', []):
            pe = PrivateEnroll.objects.filter(
                order=order.pk,
                date=item.get('selectedDate'),
                time_from=item.get('timeFrom'),
                time_to=item.get('timeTo'),
            )
            if pe:
                keep_pe.append(pe[0].pk)
        PrivateEnroll.objects.filter(
            order=order.pk, status='requested'
        ).exclude(pk__in=keep_pe).delete()

        enr_objs = {}
        num = 0
        for x in PrivateEnroll.objects.filter(order=order.pk).values('date', 'time_from', 'status'):
            if not enr_objs.get(x['date']):
                enr_objs[x['date']] = {}
            enr_objs[x['date']][x['time_from']] = x
            if x['status'] != 'rejected':
                num += 1

        overbooked = False
        # link = settings.FULL_URL + '/dashboard/teach/classes'
        key = str(uuid.uuid1())
        link = settings.FULL_URL + '/unauth_teacher/confirm_lessons/%s' % key
        new_dates = []
        total_available = order.num_lessons
        if order.interval == 'week' and order.interval_count == 1:
            # check total number of lessons available, but must be checked number of lessons per interval
            total_available = order.data['package']['classesPerInterval'] * order.data['package']['numberOfIntervals']

        for item in data.get('dates', []):
            enr_data = {
                'order': order.pk,
                'date': item.get('selectedDate'),
                'time_from': item.get('timeFrom'),
                'time_to': item.get('timeTo'),
                'secret': key,
            }
            if enr_objs.get(enr_data['date']) and enr_objs[enr_data['date']].get(enr_data['time_from']):
                # already exists
                continue

            x = datetime.strptime('%s %s' % (enr_data['date'], enr_data['time_from']), '%Y-%m-%d %H:%M')
            x = class_tz.localize(x)

            if x <= datetime.now(class_tz):
                # no actions in past
                continue

            if total_available <= num:
                overbooked = True
                continue
            num += 1
            enr_data['time_from_gmt'] = x

            pes = PrivateEnrollSerializer(data=enr_data)
            pes.is_valid(raise_exception=True)
            pe = pes.save()

            new_dates.append(format_date_time(pe.date, pe.time_from))

        if new_dates:
            date_tz = pe.order.klass.get_timezone()
            # Teacher requested date notification
            text = """Teachbeach: It’s sunny! %s has booked
 a lesson/s requesting on %s %s. Respond at %s""" % (
                order.user.first_name,
                ' '.join(new_dates),
                date_tz,
                link,
            )
            if pe.order.klass.teacher.user.phone:
                send_text(
                    text,
                    pe.order.klass.teacher.user.phone,
                )
            if pe.order.klass.teacher.phone:
                send_text(
                    text,
                    pe.order.klass.teacher.phone,
                )
            email_list = [pe.order.klass.teacher.user.email]
            if pe.order.klass.teacher.email:
                email_list.append(pe.order.klass.teacher.email)
            if order.is_subscription:
                email_subj = "Its sunny! %s has booked a %s subscription" % (
                    order.user.first_name,
                    'weekly' if order.interval == 'week' else 'monthly',
                )
            else:
                email_subj = "Its sunny! %s requests a private sesson" % (
                    order.user.first_name,
                )

            sign = get_message_sign(request, CompanyProfile)
            if order.is_subscription:
                email_body = """Hi %s, 
%s %s %s has booked a %s, requesting:
%s
Time zone: %s

Please respond within hours to build a great relationship 
%s

Powered by Teachbeach 
The fun way to earn and learn
                """ % (
                    order.klass.teacher.first_name,
                    order.user.first_name,
                    order.user.phone,
                    order.user.email,
                    "weekly for %s weeks subscription" % order.data['package']['numberOfIntervals']*order.interval_count if order.interval == 'week' else 'monthly subscription',
                    "\n ".join(new_dates),
                    date_tz,
                    # temporary disabled
                    # order.learnerNeeds,
                    link,
                )
            else:
                email_body = """Hi %s, 
%s %s %s has booked (%s)  private session%s requesting: 
%s
Time zone: %s

Please respond within hours to build a great relationship 
%s

Powered by Teachbeach 
The fun way to earn and learn
""" % (
                order.klass.teacher.first_name,
                order.user.first_name,
                order.user.phone,
                order.user.email,
                num,
                's' if num > 1 else '',
                "\n ".join(new_dates),
                date_tz,
                #temporary disabled
                #order.learnerNeeds,
                link,
            )
            send_mail_reply_to(
                email_subj,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                email_list,
                fail_silently=True,
                reply_to=[order.user.email],
            )
            # to student
            email_subj = "%s received your request for %s" % (
                order.klass.teacher.first_name,
                order.klass,
            )
            email_body = """Hi %s, 
We received your request for private session%s in %s on: 

%s
Time zone: %s

We look forward to working with you! You’ll get a message with confirmation or check the status here: %s 
%s

All the best, 

%s 
%s
%s""" % (
                order.user.first_name,
                's' if num > 1 else '',
                order.klass,
                "\n ".join(new_dates),
                date_tz,
                settings.FULL_URL + '/dashboard/learn/classes',
                'Your zoom link: ' + order.klass.zoom_link if order.klass.class_type == 'online' and order.klass.zoom_link else '',
                order.klass.teacher.first_name,
                order.klass.teacher.phone or order.klass.teacher.user.phone,
                order.klass.teacher.email or order.klass.teacher.user.email,
            )
            send_mail_reply_to(
                email_subj,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [order.user.email],
                fail_silently=True,
                reply_to=[order.klass.teacher.email or order.klass.teacher.user.email],
            )
        order.save()
        order.update_reserved_lessons()

        return Response({
            'status': True,
            'overbooked': overbooked,
            'isFirstLesson': is_first_lesson
        })

class PrivateEnrollConfirmView(generics.CreateAPIView):
    serializer_class = PrivateEnrollSerializer

    def post(self, request, pk):
        pe = PrivateEnroll.objects.get(
            pk=pk,
            order__klass__teacher__user=request.user
        )

        class_tz = pytz.timezone(pe.order.klass.timezone)
        x = datetime.strptime('%s %s' % (pe.date, pe.time_from), '%Y-%m-%d %H:%M')
        x = class_tz.localize(x)

        status = False
        if pe.status == 'requested' and x >= datetime.now(class_tz):
            pe.status = 'approved'
            pe.save()
            status = True

            dt_tz = pe.order.klass.get_timezone()
            # Lesson times approved notification
            teacher_message = """Message from teacher: %s
""" % (request.data.get('message'),) if request.data.get('message') else ''
            dt = format_date_time(pe.date, pe.time_from)
            link = settings.FULL_URL + '/dashboard/learn/classes'
            link2 = settings.FULL_URL + '/class/' + str(pe.order.klass.pk)
            subj_text = 'TeachBeach: Your lesson is booked on %s %s %s' % (
                dt,
                dt_tz,
                link,
            )
            sign = get_message_sign(request, CompanyProfile)
            email_subj = "Heads up! %s is scheduled for %s" % (
                pe.order.klass,
                x.strftime('%B %d'),
            )
            email_text = """Hi %s, 

%s with %s is scheduled on: 
%s
Time zone: %s

%s

Sync to calendar here: %s
Check out the class here: %s


All the best, 

%s
%s 
%s 

%s
""" % (
    pe.order.user.first_name,
    pe.order.klass,
    pe.order.klass.teacher.user.first_name,
    dt, dt_tz,
    teacher_message,
    link,
    link2,
    pe.order.klass.teacher.first_name,
    pe.order.klass.teacher.phone or pe.order.klass.teacher.user.phone,
    pe.order.klass.teacher.email or pe.order.klass.teacher.user.email,
    sign,
)

            if pe.order.user.phone:
                send_text(
                    subj_text,
                    pe.order.user.phone,
                )
            send_mail_reply_to(
                email_subj,  # subject
                email_text,  # body
                settings.DEFAULT_FROM_EMAIL,
                [pe.order.user.email],
                fail_silently=True,
                reply_to=[pe.order.klass.teacher.email or pe.order.klass.teacher.user.email],
            )

            pe.order.update_reserved_lessons()

        return Response({
            'status': status
        })


class PrivateEnrollRejectView(generics.CreateAPIView):
    serializer_class = PrivateEnrollSerializer

    def post(self, request, pk):
        pe = PrivateEnroll.objects.get(
            pk=pk,
            order__klass__teacher__user=request.user
        )
        status = False
        if pe.status == 'requested':
            pe.status = 'rejected'
            pe.decline_reason = request.data.get('reason', '')
            pe.save()
            status = True

            city_link = settings.FULL_URL + '/learners/search/online/none/0/'
            if pe.order.klass.address_city:
                city_link = settings.FULL_URL + '/learners/search/%s/%s/0/' % (
                    urllib.parse.quote(pe.order.klass.address_city),
                    pe.order.klass.address_state,
                )
            if pe.order.klass.class_type == 'online':
                city_link = settings.FULL_URL + '/learners/search/online/none/0/'

            # Decline notice notification
            subj = 'Whoops.... that\'s not going to work!'
            link = settings.FULL_URL + '/learners/%s/7/%s' % (
                pe.order.klass.pk,
                pe.order.pk,
            )
            sign = get_message_sign(request, CompanyProfile)
            text = """Whoops... That’s not going to work! 
Message from %s: %s 
Reschedule link: %s
Find another teacher link: %s


%s
""" % (
                pe.order.klass.teacher.first_name,
                pe.decline_reason,
                link,
                city_link,
                sign,
            )
            if pe.order.user.phone:
                send_text(
                    text,
                    pe.order.user.phone,
                )
            email_text = """Hi %s, 

%s 

All the best, 
%s

Reschedule: %s 
Find another teacher: %s

%s""" % (
                pe.order.user.first_name,
                pe.decline_reason,
                pe.order.klass.teacher.first_name,
                link,
                city_link,
                sign,
            )
            send_mail_reply_to(
                subj,  # subject
                email_text,  # body
                settings.DEFAULT_FROM_EMAIL,
                [pe.order.user.email],
                fail_silently=True,
                reply_to=[pe.order.klass.teacher.email or pe.order.klass.teacher.user.email],
            )

            pe.order.update_reserved_lessons()

        return Response({
            'status': status
        })


class GroupEnrollView(generics.ListAPIView):
    def post(self, request):
        data = request.data
        order = ClassLearner.objects.get(
            pk=data.get('orderId'),
            user=request.user
        )
        enr_objs = {}
        new_enr = {}
        for x in data.get('selectedLessons'):
            items = x.split('_')
            date = items[0]
            times = items[1].split('-')
            if not new_enr.get(date):
                new_enr[date] = {}
            new_enr[date][times[0]] = True
        num = 0
        overbooked = False
        changed = False
        dates = []
        for x in GroupEnroll.objects.filter(order=order.pk).values('date', 'time_from', 'status', 'pk'):
            if not enr_objs.get(x['date']):
                enr_objs[x['date']] = {}
            if (not new_enr.get(x['date']) or not new_enr[x['date']].get(x['time_from'])) and x['status'] != 'rejected':
                # delete enrollment
                item = GroupEnroll.objects.get(pk=x['pk'])
                item.status = 'rejected'
                item.save()
                continue
            enr_objs[x['date']][x['time_from']] = x
            if x['status'] != 'rejected':
                num += 1
        is_first_lesson = len(ClassLearner.objects.filter(user=request.user)) == 1 and order.reserved_lessons == 0
        for x in data.get('selectedLessons'):
            items = x.split('_')
            date = items[0]
            times = items[1].split('-')

            class_tz = pytz.timezone(order.klass.timezone)
            x = datetime.strptime('%s %s' % (date, times[0]), '%Y-%m-%d %H:%M')
            x = class_tz.localize(x)

            enr_data = {
                'order': order.pk,
                'date': date,
                'time_from': times[0],
                'time_to': times[1],
                'time_from_gmt': x,
            }

            if x <= datetime.now(class_tz):
                # no actions in past
                continue

            if enr_objs.get(enr_data['date']) and enr_objs[enr_data['date']].get(enr_data['time_from']):
                # already exists
                continue

            if order.num_lessons <= num:
                overbooked = True
                continue
            num += 1

            ges = GroupEnrollSerializer(data=enr_data)
            ges.is_valid(raise_exception=True)
            ges.save()
            changed = True
            d_str = format_date_time_from_to(enr_data['date'], enr_data['time_from'], enr_data['time_to'])
            dates.append(d_str)

        if changed:
            dates_tz = order.klass.get_timezone()
            link = settings.FULL_URL + '/dashboard/learn/classes'
            text = """It’s sunny! You are booked for %s on %s, time zone: %s,  %s. Sync to calendar.

Powered by Teachbeach. 
""" % (
                order.klass,
                "\n".join(dates),
                dates_tz,
                link,
            )
            sign = get_message_sign(request, CompanyProfile)
            email_subj = 'It’s sunny! You are booked for %s' % order.klass
            email_body = """Hi %s, 

Confirmed! You are booked for "%s with %s" on:
%s
Time zone: %s
%s

Sync to your personal calendar here %s
Keep track on your own dashboard here: %s

Look forward to working with you! 

All the best, 

%s
%s
%s
""" % (
    order.user.first_name,
    order.klass,
    order.klass.teacher.first_name,
    "\n".join(dates),
    dates_tz,
    'Please use this link to join the session: ' + order.klass.zoom_link if order.klass.zoom_link else ('Zoom link to come! ' if order.klass.class_type == 'online' else ''),
    settings.FULL_URL + '/dashboard/learn/calendar',
    link,
    order.klass.teacher.first_name,
    order.klass.teacher.phone or order.klass.teacher.user.phone,
    order.klass.teacher.email or order.klass.teacher.user.email,
)
            if order.user.phone:
                send_text(
                    text,
                    order.user.phone,
                )
            email_list = [order.user.email]

            send_mail_reply_to(
                email_subj,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                email_list,
                fail_silently=True,
                reply_to=[order.klass.teacher.email or order.klass.teacher.user.email],
            )

            # teacher notificaions
            link = settings.FULL_URL + '/dashboard/teach/classes'
            text = "Teachbeach: It’s sunny! %s has enrolled in %s on %s %s" % (
                order.user.first_name,
                order.klass,
                "\n".join(dates),
                link,
            )
            sign = get_message_sign(request, CompanyProfile)
            sender_company = get_email_company_name(order.klass.pk)
            email_subj = "It’s sunny! %s has enrolled in %s" % (
                order.user.first_name,
                order.klass,
            )
            email_body = """Hi %s

%s and has enrolled in %s: 
%s
Timezone: %s

%s at %s or %s has been added to your CRM . 

Sync to personal calendar here: 
Manage your TeachBeach schedule here %s

Express from %s
Join for the classes. Stay for the community.

Thanks! 
The team at %s
""" % (
        order.klass.teacher.first_name,
        order.user.first_name,
        order.klass,
        "\n".join(dates),
        order.klass.timezone,
        order.user.first_name,
        order.user.email,
        order.user.phone,
        link,
        sender_company,
        sender_company,
    )
            if order.klass.teacher.user.phone:
                send_text(
                    text,
                    order.klass.teacher.user.phone,
                )

            email_list = [order.klass.teacher.user.email]
            if order.klass.teacher.email:
                email_list.append(order.klass.teacher.email)

            send_mail_reply_to(
                email_subj,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                email_list,
                fail_silently=True,
                reply_to=[order.user.email],
            )


        order.update_reserved_lessons()

        return Response({
            'status': True,
            'overbooked': overbooked,
            'isFirstLesson': is_first_lesson
        })


class LearnerClassesView(generics.RetrieveAPIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=401)

        pr = PrivateEnroll.objects.filter(order__user=request.user).order_by('date', 'time_from')
        gr = GroupEnroll.objects.filter(order__user=request.user).order_by('date', 'time_from')
        orders = ClassLearner.objects.filter(user=request.user)
        memberships = MembershipStudent.objects.filter(student=request.user)
        comp_admins = [m.membership.owner_user_id for m in memberships]
        if len(comp_admins):
            membership_classes = ClassSerializer(Class.objects.filter(teacher__in=Teacher.objects.filter(Q(user__in=comp_admins) or Q(user__belongs_to__in=comp_admins))), many=True).data
        else:
            membership_classes = []
        res = {
            'private_enroll': PrivateEnrollSerializer(pr, many=True).data,
            'group_enroll': GroupEnrollSerializer(gr, many=True).data,
            'orders': ClassLearnerSerializer(orders, many=True).data,
            'membership_classes': membership_classes,
        }
        return Response(res)


class TeacherStudentsView(generics.RetrieveAPIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=401)

        teachers = Teacher.objects.filter(user=request.user)
        if request.user.is_company:
            teachers = teachers | Teacher.objects.filter(user__belongs_to=request.user.company.pk)

        orders = ClassLearner.objects.filter(
            klass__teacher__in=teachers
        )

        customers = ClassLearner.objects.filter(
            klass__teacher__in=teachers,
            status='succeeded',
        ).values('user')

        all_users = orders.values('user')
        klasses = orders.values('klass')
        order_classes = Class.all_objects.filter(pk__in=klasses, deleted_at=None)

        teacher_classes = Class.objects.filter(teacher__in=teachers)

        students = MembershipStudent.objects.filter(membership__owner_user__pk=request.user.pk)
        member_ids = [s.student_id for s in students.filter(is_active=True)]
        canceled_member_ids = [s.student_id for s in students.filter(is_active=False)]

        is_registered = [x.pk for x in User.objects.filter(class_id__in=teacher_classes)]
        is_unregistered = [x.pk for x in User.objects.filter(managed_by__contains=[request.user.pk])]
        is_prospects = [x.pk for x in User.objects.filter(Q(managed_by__contains=[request.user.pk]) | Q(class_id__in=teacher_classes))]

        a = User.objects.filter(Q(pk__in=all_users)|Q(class_id__in=teacher_classes)|Q(managed_by__contains=[request.user.pk]))
        try:
            membership = MembershipSerializer(Membership.objects.get(owner_user=request.user)).data
        except Membership.DoesNotExist:
            membership = None
        res = {
            'all': [{**x,
                     'isMember': x['id'] in member_ids,
                     'isCanceledMember': x['id'] in canceled_member_ids,
                     'isCustomer': x['id'] in [y['user'] for y in customers] + member_ids,
                     'isRegistered': x['id'] in is_registered and x['id'] not in member_ids and x['id'] not in [y['user'] for y in customers],
                     'isUnregistered': x['id'] in is_unregistered and x['id'] not in member_ids and x['id'] not in [y['user'] for y in customers],
                     'isProspect': x['id'] in is_prospects and x['id'] not in member_ids and x['id'] not in [y['user'] for y in customers],
                     'isStudent': x['id'] in all_users,
                     } for x in UserAllClassesSerializer(a, many=True).data],
            'orders': ClassLearnerNoDataClassSerializer(orders, many=True).data,
            'classes': ClassShortSerializer(teacher_classes, many=True).data,
            'deleted': [x['student_id'] for x in request.user.deleted_students.values('student_id')],
            'membership': membership,
        }
        return Response(res)


class TeacherClassesView(generics.RetrieveAPIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=401)

        if request.user.is_company:
            teachers = Teacher.objects.filter(Q(user=request.user) | Q(user__belongs_to=request.user.company.pk))
        else:
            teachers = Teacher.objects.filter(user=request.user)
        if not teachers:
            teacher = Teacher(user=request.user)
            teacher.save()
            teachers = Teacher.objects.filter(user=request.user)

        orders = ClassLearner.objects.filter(
            klass__teacher__in=teachers,
            klass__deleted_at=None,
        )

        today = datetime.now().strftime("%Y-%m-%d")

        pr = PrivateEnroll.objects.filter(
            order__klass__teacher__in=teachers,
            order__klass__deleted_at=None,
            # date__gte=today,
        )
        gr = GroupEnroll.objects.filter(
            order__klass__teacher__in=teachers,
            order__klass__deleted_at=None,
            # date__gte=today,
        )

        new_orders = ClassLearner.objects.filter(
            klass__teacher__in=teachers,
            klass__deleted_at=None,
        ).exclude(
            pk__in=gr.values('order')
        ).exclude(
            pk__in=pr.values('order')
        ).filter(
            data__isRemovedNotification__isnull=True
        )

        classes = Class.objects.filter(teacher__in=teachers)

        amount = ClassLearner.objects.filter(
            klass__teacher__in=teachers,
            no_pay=False,
            status='succeeded',
            paid_status=1,
        ).aggregate(sum=Sum('amount'))
        bank_message = ''
        if amount['sum'] and not request.user.has_external_account:
            bank_message = 'You have $%s waiting ' % (amount['sum'] or 0)

        bm = BoostMembership.objects.filter(user=request.user, valid=True).last()
        boosted = classes.filter(is_boosted=True).count()

        res = {
            'private_enroll':  PrivateEnrollDetailsSerializer(pr, many=True).data,
            'group_enroll':  GroupEnrollDetailsSerializer(gr, many=True).data,
            'classes': ClassShortSerializer(classes, many=True).data,
            'bank_message': bank_message,
            'boost_classes_num': None,
            'new_orders': ShortOrderSerializer(new_orders, many=True).data,
            'orders': ClassLearnerNoDataClassSerializer(orders, many=True).data,
        }
        if bm:
            res['boost_classes_num'] = bm.num_classes - boosted
        return Response(res)


class SelectedTeacherClassesView(generics.RetrieveAPIView):
    queryset = ''

    def get(self, request, pk):
        c = Class.objects.filter(teacher=pk)
        return Response(ClassFullSerializer(c, many=True).data)


class SelectedCompanyClassesView(generics.RetrieveAPIView):
    queryset = ''

    def get(self, request, pk):
        c = Class.objects.filter(teacher__user__company=pk)
        return Response(ClassFullSerializer(c, many=True).data)


class TeacherStripeAccountView(generics.ListAPIView):
    # serializer_class = None
    serializer_class = ClassLearnerSerializer

    def get(self, request):
        acc_id = request.user.stripe_account_id
        if acc_id:
            stripe.api_key = os.environ['STRIPE_SECRET_KEY']
            account = stripe.Account.retrieve(acc_id)
        else:
            account = None
        amount = ClassLearner.objects.filter(
            klass__teacher__user=request.user,
            no_pay=False,
            status='succeeded',
            paid_status=1,
        ).aggregate(sum=Sum('amount'))
        bank_message = ''
        if amount['sum']:
            bank_message = 'You have $%s waiting ' % (amount['sum'] or 0)

        return Response({
            'account': account,
            'bank_message': bank_message,
        })

    def post(self, request):
        # https://stripe.com/docs/connect/testing
        data = request.data
        stripe.api_key = os.environ['STRIPE_SECRET_KEY']
        if not request.user.first_name or not request.user.last_name:
            return Response({
                'status': False,
                'err': 'Make sure you filled out first and last name in "My Profile"',
            })
        if not request.user.stripe_account_id:
            url = 'https://teachbeach.com/'
            if request.user.is_company:
                cp = CompanyProfile.objects.get(user=request.user)
                url += 'company_profile/%s' % cp.pk
            else:
                teacher = Teacher.objects.get(user=request.user)
                url += 'teacher_profile/%s' % teacher.pk

            account = stripe.Account.create(
                country='US',
                type='custom',
                business_type='individual',
                individual={
                    'email': request.user.email,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                },
                requested_capabilities=['transfers'],
                tos_acceptance={
                    'date': int(time.time()),
                    'ip': get_client_ip(request),
                },
                business_profile={
                    'url': url,
                }
            )
            request.user.stripe_account_id = account['id']
            request.user.save()
        else:
            account = stripe.Account.retrieve(request.user.stripe_account_id)
        external_account = {
            'object': 'bank_account',
            'country': 'US',
            'currency': 'usd',
            'account_holder_name': data.get('accountName'),
            'account_holder_type': 'individual',
            'routing_number': data.get('routingNumber', '').strip(),
            'account_number': data.get('bankAccountNumber', '').strip(),
        }

        status = True
        err = None
        try:
            stripe.Account.modify(
                request.user.stripe_account_id,
                external_account=external_account
            )
            request.user.has_external_account = True
            request.user.save()
        except stripe.error.InvalidRequestError as e:
            status = False
            err = e.user_message

        if not account['tos_acceptance'].get('date'):
            url = 'https://teachbeach.com/'
            if request.user.is_company:
                cp = CompanyProfile.objects.get(user=request.user)
                url += 'company_profile/%s' % cp.pk
            else:
                teacher = Teacher.objects.get(user=request.user)
                url += 'teacher_profile/%s' % teacher.pk
            stripe.Account.modify(
              request.user.stripe_account_id,
              tos_acceptance={
                'date': int(time.time()),
                'ip': get_client_ip(request),
              },
              business_profile={
                'url': url,
              }
            )

        return Response({
            'status': status,
            'err': err,
        })


class MessageViewSet(viewsets.ModelViewSet):
    filter_backends = (MessageUserFilter,)

    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class DraftClassViewSet(viewsets.ModelViewSet):
    filter_backends = (UserFilter,)

    def list(self, request):
        drafts = None
        if request.user.is_authenticated:
            draft_classes = DraftClass.objects.filter(user=request.user)
            drafts = DraftClassSerializer(draft_classes, many=True).data
        return Response({
            'drafts': drafts,
        })

    def create(self, request):
        draft, _ = DraftClass.objects.get_or_create(
            user=request.user
        )
        draft.class_data = request.data.get('class_data')
        draft.save()

        return Response({
            'status': True,
        })

    queryset = DraftClass.objects.all()
    serializer_class = DraftClassSerializer


class CloneClassView(generics.ListAPIView):
    def post(self, request, pk):
        c = Class.objects.get(pk=pk, teacher__user=request.user)
        draft, _ = DraftClass.objects.get_or_create(
            user=request.user
        )
        if c.class_data.get('schedule_dates'):
            del c.class_data['schedule_dates']
        if c.class_data.get('schedule_from'):
            del c.class_data['schedule_from']
        if c.class_data.get('schedule_to'):
            del c.class_data['schedule_to']
        if c.class_data.get('weekdays_schedule'):
            del c.class_data['weekdays_schedule']

        draft.class_data = c.class_data
        draft.save()

        return Response({
            'status': True,
            'class': DraftClassSerializer(draft).data,
        })


class PaymentCardsView(generics.RetrieveAPIView):
    queryset = ''

    def get(self, request):
        stripe.api_key = os.environ['STRIPE_SECRET_KEY']
        uc = UserCard.objects.filter(user=request.user)
        sources = []
        c = {}
        if uc and uc[0].customer_id:
            c = stripe.Customer.retrieve(uc[0].customer_id)
            sources = c['sources'].get('data')

        return Response({
            'default': c.get("default_source"),
            'sources': sources
        })


class CsvMembersExportView(APIView):
    def get(self, request):
        memberships = MembershipStudent.objects.filter(student=request.user)

        from_date = None
        to_date = None
        if request.GET.get('from_date'):
            from_date = datetime.strptime(request.GET['from_date'], '%Y-%m-%d')
        if request.GET.get('to_date'):
            to_date = datetime.strptime(request.GET['to_date'], '%Y-%m-%d')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="members_report.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'First Name', 'Last Name', 'Date', '$', 'email', 'phone'
        ])
        for m in memberships:
            for inv in m.invoices:
                created = datetime.fromtimestamp(inv['created'])
                if (not from_date or from_date < created) and (not to_date or to_date > created):
                    writer.writerow([
                        m.student.first_name,
                        m.student.last_name,
                        created,
                        inv['amount_paid'],
                        m.student.email,
                        m.student.phone,
                    ])

        return response


class CsvStudentExportView(APIView):
    def get(self, request):
        classes = Class.objects.filter(teacher__user=request.user)

        from_date = None
        to_date = None
        if request.GET.get('from_date'):
            from_date = datetime.strptime(request.GET['from_date'], '%Y-%m-%d')
            classes = classes.filter(
                Q(until_date__isnull=True) |
                Q(until_date__gte=from_date)
            )
        if request.GET.get('to_date'):
            to_date = datetime.strptime(request.GET['to_date'], '%Y-%m-%d')
            classes = classes.filter(start_date__lte=to_date)
        users = ClassLearner.objects.filter(klass__in=classes)
        users = ClassLearner.objects.filter(klass__in=classes).distinct('user__pk').values_list('user__pk', flat=True)
        users = User.objects.filter(pk__in=users)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students_report.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'First Name', 'Last Name', 'Classes', '# classes taken', '$', 'email', 'phone'
        ])
        for u in users:
            classes_taken = {}
            revenue = 0
            orders = ClassLearner.objects.filter(
                klass__in=classes,
                user=u,
            )
            if from_date:
                orders = orders.filter(created_at__gte=from_date)
            if to_date:
                orders = orders.filter(created_at__lte=to_date)
            for o in orders:
                if not o.no_pay:
                    revenue += o.amount
                classes_taken[o.klass.pk] = o.klass.name
                if o.num_lessons != o.reserved_lessons:
                    classes_taken[o.klass.pk] = o.klass.name+(" (%s/%s lessons left)" % (o.num_lessons-o.reserved_lessons, o.num_lessons))

            writer.writerow([
                u.first_name,
                u.last_name,
                ', '.join(classes_taken.values()),
                reduce(lambda total, o: total+o.num_lessons, orders, 0),
                #len(classes_taken.keys()),
                revenue,
                u.email,
                u.phone,
            ])

        return response


class CsvExportView(APIView):
    def get(self, request):
        classes = Class.objects.filter(teacher__user=request.user)

        from_date = None
        to_date = None
        if request.GET.get('from_date'):
            from_date = datetime.strptime(request.GET['from_date'], '%Y-%m-%d')
            classes = classes.filter(
                Q(until_date__isnull=True) |
                Q(until_date__gte=from_date)
            )
        if request.GET.get('to_date'):
            to_date = datetime.strptime(request.GET['to_date'], '%Y-%m-%d')
            classes = classes.filter(start_date__lte=to_date)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="teacher_report.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Date', 'Teacher Name', 'Class Name', '#Lessons', 'Student', 'Revenue', 'Paid'
        ])
        total_num_classes = 0
        revenue = 0
        total_students = 0
        total_paid = 0
        for c in classes:
            class_revenue = 0
            students = 0
            orders = ClassLearner.objects.filter(klass=c)
            if from_date:
                orders = orders.filter(created_at__gte=from_date)
            if to_date:
                orders = orders.filter(created_at__lte=to_date)
            for o in orders:
                class_revenue = 0 if o.no_pay else o.amount
                # if not o.no_pay:
                    # class_revenue += o.amount
                # students += 1
                students = 1
                num_classes = o.num_lessons

                # num_classes += 1
                total_students += students
                total_num_classes += num_classes
                revenue += class_revenue
                paid = ''

                if o.is_subscription:
                    class_revenue = f"{class_revenue} (subscription)"
                    paid = o.total_paid or 0
                    total_paid += paid
                else:
                    if o.paid_status == 2:
                        paid = o.payment.created_at.strftime('%b %d, %Y')
                        total_paid += o.amount
                teacher = "%s %s" % (c.teacher.first_name, c.teacher.last_name)
                student = "%s %s" % (o.user.first_name, o.user.last_name)
                writer.writerow([o.created_at.strftime('%b %d, %Y'), teacher, c.name, num_classes, student, class_revenue, paid])
        writer.writerow(['Total', '', '', total_num_classes, total_students, revenue, total_paid])

        return response


class TeacherClassMessageView(APIView):
    def post(self, request, pk):
        if request.user.is_company:
            klass = Class.objects.get(
                Q(pk=pk), Q(teacher__user=request.user) | Q(teacher__user__belongs_to=request.user.company.pk)
            )
        else:
            klass = Class.objects.get(
                pk=pk, teacher__user=request.user
            )
        text = request.data.get('message') + """
To reply, please text %s directly at %s.""" % (
            klass.teacher.first_name,
            klass.teacher.phone or klass.teacher.user.phone,
        )
        users = ClassLearner.objects.filter(klass=klass).values('user').distinct()
        n = 0
        for u in User.objects.filter(pk__in=users):
            n += 1
            if u.phone:
                send_text(
                    text,
                    u.phone,
                )
            email_list = [u.email]

            send_mail_reply_to(
                'Information about class',  # subject
                text,  # body
                settings.DEFAULT_FROM_EMAIL,
                email_list,
                fail_silently=True,
                reply_to=[klass.teacher.email or klass.teacher.user.email],
            )
        if request.data.get('copyMe'):
            send_mail(
                'Copy: Information about class',  # subject
                text,  # body
                settings.DEFAULT_FROM_EMAIL,
                [klass.teacher.email or klass.teacher.user.email],
                fail_silently=True,
            )
        return Response({
            'num_students': n,
            'status': True,
        })


class SearchView(APIView):
    def get(self, request, q):
        companies = CompanyProfile.objects.filter(name__icontains=q)
        teachers = Teacher.objects.filter(Q(first_name__icontains=q)|Q(last_name__icontains=q))
        return Response({
            'teachers': TeacherSerializer(teachers, many=True).data,
            'companies': CompanyProfileSerializer(companies, many=True).data,
        })


class ServiceFeeView(APIView):
    def post(self, request):
        amount = float(request.data.get('amount'))
        fee = 0.1 * amount
        if amount > 90:
            fee = 0.03 * (amount - 90) + 9

        return Response({
            'fee': fee,
        })



class BuyMembershipView(APIView):
    OPTIONS = [
        {'id': 1, 'num_classes': 1, 'is_monthly': True, 'amount': 10, 'name': 'Solo'},
        {'id': 2, 'num_classes': 5, 'is_monthly': True, 'amount': 25, 'name': 'Academy'},
        {'id': 3, 'num_classes': 20, 'is_monthly': True, 'amount': 100, 'name': 'University'},
        {'id': 4, 'num_classes': 1, 'is_monthly': False, 'amount': 65, 'name': 'Single'},
    ]

    def get(self, request):
        bm = BoostMembership.objects.filter(
            user=request.user,
            valid=True,
        ).last()
        c = Class.objects.filter(teacher__user=request.user).last()
        can_book = None
        if c:
            can_book = c.can_book

        options = self.OPTIONS
        current_option = BoostMembershipSerializer(bm).data if bm else None if bm else None

        for x in options:
            if not current_option or current_option.get('num_classes') < x['num_classes']:
                x['is_available'] = True
            else:
                x['is_available'] = False
            if x['id'] == 4:
                x['is_available'] = True

        return Response({
            'can_book': can_book,
            'available_options': self.OPTIONS,
            'current_option': current_option,
        })

    def post(self, request):
        stripe.api_key = os.environ['STRIPE_SECRET_KEY']
        trial = True

        current_bm = BoostMembership.objects.filter(user=request.user, valid=True, is_monthly=True).last()

        data = request.data
        token = data.get('token')
        card_id = data.get('card_id')

        uc, created = UserCard.objects.get_or_create(user=request.user)

        if not trial and token and card_id == 'new_card' and token.get('card'):
            try:
                if not uc.customer_id:
                    customer = stripe.Customer.create(
                        source=token['id'],
                        email=request.user.email,
                    )
                    card_id = customer['default_source']
                    uc.customer_id = customer.id
                    uc.save()
                else:
                    card = stripe.Customer.create_source(
                        uc.customer_id,
                        source=token['id']
                    )
                    card_id = card['id']
            except stripe.error.CardError as e:
                return Response({'success': False, 'error_message': e.user_message})

        # cost in cents
        option_id = data['option_id']
        if option_id < 1 or option_id > 4:
            return Response({'success': False, 'error_message': 'Invalid option selected'})
        options = {}
        for x in self.OPTIONS:
            options[x['id']] = x
        option = options[option_id]
        cost = option['amount']

        desc = 'Teachbeach membership'

        charge = None
        stripe_id = None
        status = None
        cost = 0
        status = 'trial'
        if not trial:
            if not option['is_monthly']:
                try:
                    charge = stripe.Charge.create(
                        amount=cost*100,
                        currency='usd',
                        description=desc,
                        customer=uc.customer_id,
                        source=card_id,
                    )
                except stripe.error.CardError as e:
                    return Response({'success': False, 'error_message': e.user_message, 'order_id': c.id})

                stripe_id = charge['id']
                status = charge['status']
            else:
                # monthly payment
                plan = stripe.Plan.create(
                  amount=cost*100,
                  currency="usd",
                  interval="month",
                  product={"name": "Teachbeach membership"},
                )

                subs = stripe.Subscription.create(
                    customer=uc.customer_id,
                    items=[{"plan": plan.id}],
                )
                status = subs['status']
                stripe_id = subs['id']

        checkout = {
            'num_classes': option['num_classes'],
            'data': data,
            'user': request.user.pk,
            'amount': cost,
            'is_monthly': option['is_monthly'],
            'stripe_id': stripe_id,
            'status': status,
            'option_id': option['id'],
        }


        bm = BoostMembershipSerializer(data=checkout)
        bm.is_valid(raise_exception=True)
        c = bm.save()

        # Sale notification
        text = 'TeachBeach: %s has bought membership for $%s' % (
            c.user,
            cost,
        )
        send_text(
            text,
            settings.TEXT_NOTIFICATIONS
        )
        send_mail(
            text,  # subject
            text,  # body
            settings.DEFAULT_FROM_EMAIL,
            ['alisacromer@gmail.com',],
            fail_silently=True,
        )

        if current_bm:
            # cancel previous subscription
            if current_bm.stripe_id:
                res = stripe.Subscription.delete(current_bm.stripe_id)
            current_bm.valid = False
            current_bm.status = 'canceled'
            current_bm.save()

        return Response({'success': True})


class CancelMembershipView(APIView):
    def post(self, request):
        stripe.api_key = os.environ['STRIPE_SECRET_KEY']

        data = request.data
        pk = data.get('id')
        bm = BoostMembership.objects.get(user=request.user, pk=pk)
        res = stripe.Subscription.delete(bm.stripe_id)
        bm.valid = False
        bm.status = 'canceled'
        bm.save()

        text = 'TeachBeach: %s cancelled membership' % (
            request.user,
        )
        # send_text(
        #     text,
        #     settings.TEXT_NOTIFICATIONS
        # )
        send_mail(
            text,  # subject
            text,  # body
            settings.DEFAULT_FROM_EMAIL,
            ['alisacromer@gmail.com', ],
            fail_silently=True,
        )

        return Response({'success': True})


class BuyEmailBoostView(APIView):
    OPTIONS = [
        {'id': 1, 'num_classes': 1, 'is_monthly': False, 'amount': 350, 'name': 'Single'},
    ]

    def get(self, request):
        return Response({
            'available_options': self.OPTIONS,
        })

    def post(self, request):
        stripe.api_key = os.environ['STRIPE_SECRET_KEY']

        data = request.data
        token = data.get('token')
        card_id = data.get('card_id')
        class_id = data.get('class_id')
        klass = Class.objects.get(pk=class_id, teacher__user=request.user)

        em_boost = EmailBoost.objects.filter(klass_id=class_id)
        if em_boost.count() > 0:
            return Response({'success': False, 'error_message': 'Class already boosted'})

        uc, created = UserCard.objects.get_or_create(user=request.user)

        if token and card_id == 'new_card' and token.get('card'):
            try:
                if not uc.customer_id:
                    customer = stripe.Customer.create(
                        source=token['id'],
                        email=request.user.email,
                    )
                    card_id = customer['default_source']
                    uc.customer_id = customer.id
                    uc.save()
                else:
                    card = stripe.Customer.create_source(
                        uc.customer_id,
                        source=token['id']
                    )
                    card_id = card['id']
            except stripe.error.CardError as e:
                return Response({'success': False, 'error_message': e.user_message})

        # cost in cents
        option_id = data.get('option_id', 1)
        if option_id != 1:
            return Response({'success': False, 'error_message': 'Invalid option selected'})
        options = {}
        for x in self.OPTIONS:
            options[x['id']] = x
        option = options[option_id]
        cost = option['amount']

        desc = 'Teachbeach email boost'

        charge = None
        stripe_id = None
        status = None
        if not option['is_monthly']:
            try:
                charge = stripe.Charge.create(
                    amount=cost*100,
                    currency='usd',
                    description=desc,
                    customer=uc.customer_id,
                    source=card_id,
                )
            except stripe.error.CardError as e:
                return Response({'success': False, 'error_message': e.user_message})

            stripe_id = charge['id']
            status = charge['status']
        else:
            # monthly payment
            plan = stripe.Plan.create(
              amount=cost*100,
              currency="usd",
              interval="month",
              product={"name": "Teachbeach email boost"},
            )

            subs = stripe.Subscription.create(
                customer=uc.customer_id,
                items=[{"plan": plan.id}],
            )
            status = subs['status']
            stripe_id = subs.id

        checkout = {
            'num_classes': option['num_classes'],
            'data': data,
            'user': request.user.pk,
            'amount': cost,
            'is_monthly': option['is_monthly'],
            'stripe_id': stripe_id,
            'status': status,
            'option_id': option['id'],
            'klass': klass.pk,
        }

        bm = EmailBoostSerializer(data=checkout)
        bm.is_valid(raise_exception=True)
        c = bm.save()

        # Sale notification
        text = 'TeachBeach: %s has bought email boost for class https://teachbeach.com/class/%s ($%s)' % (
            c.user,
            klass.pk,
            cost,
        )
        send_text(
            text,
            settings.TEXT_NOTIFICATIONS
        )
        send_mail(
            text,  # subject
            text,  # body
            settings.DEFAULT_FROM_EMAIL,
            ['alisacromer@gmail.com', ],
            fail_silently=True,
        )

        return Response({'success': True})


class BoostClassView(APIView):
    def post(self, request, pk):
        data = request.data
        option_id = data.get('boost_option_id')
        card_id = data.get('card_id')

        c = Class.objects.get(
            pk=pk, teacher__user=request.user,
        )
        # price in USD
        options = {
            1: 250,
            2: 25,
        }
        try:
            uc = UserCard.objects.get(user=request.user)
        except UserCard.DoesNotExist:
            return Response({'success': False, 'error_message': 'Add card first'})
        if not options.get(option_id):
            return Response({'success': False, 'error_message': 'Invalid option'})

        charge = None
        try:
            charge = stripe.Charge.create(
                amount=options[option_id]*100,
                currency='usd',
                description='Class boost charge',
                customer=uc.customer_id,
                source=card_id,
            )
        except stripe.error.CardError as e:
            return Response({'success': False, 'error_message': e.user_message})

        c.is_boosted = True
        c.boost_option_id = option_id
        c.save()

        # send an email
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        text = '%s requested class boost ($%s) for class https://teachbeach.com/class/%s' % (
            request.user,
            options[option_id],
            c.pk,
        )
        # if c.boost_weekday:
        #     text += ' Best day is: %s' % days[c.boost_weekday]
        send_mail(
            'Class boost requested',  # subject
            text,  # body
            settings.DEFAULT_FROM_EMAIL,
            ['alisacromer@gmail.com', 'debparthapratim0@gmail.com', ],
            fail_silently=True,
        )

        cl = ChargeLog(
            user=request.user,
            amount=options[option_id]*100,
            charge_id=charge['id'],
        )
        cl.save()

        return Response({'status': True})


class RescheduleEnrollmentView(APIView):
    def post(self, request):
        data = request.data
        Klass = GroupEnroll
        EnrSer = GroupEnrollSerializer
        if data.get('enrollment_type') == 'private':
            Klass = PrivateEnroll
            EnrSer = PrivateEnrollSerializer
        enr = Klass.objects.get(
            pk=data.get('enrollment_id'),
            order__klass__teacher__user=request.user,
        )
        date = data.get('datetime')
        enr_from = enr.time_from.split(':')
        enr_to = enr.time_to.split(':')
        duration = int(enr_to[1]) + int(enr_to[0]) * 60 - int(enr_from[1]) - int(enr_from[0]) * 60
        date_parts = date.split(' ')

        class_tz = pytz.timezone(enr.order.klass.timezone)

        x = datetime.strptime(data.get('datetime'), '%Y-%m-%d %H:%M')
        x = class_tz.localize(x)

        if x <= datetime.now(class_tz):
            # no actions in past
            return Response({'status': False, 'err': 'Can not reschedule to past'})

        enr.time_from_gmt = x
        enr.date = date_parts[0]
        enr.time_from = date_parts[1]

        new_enr_from = enr.time_from.split(':')

        enr.time_to = new_enr_from[0]
        new_time_minutes = int(new_enr_from[0])*60+int(new_enr_from[1])+duration
        new_hours = "{:02d}".format(int(math.floor(new_time_minutes/60)))
        new_minutes = "{:02d}".format(new_time_minutes % 60)
        enr.time_to = "%s:%s" % (new_hours, new_minutes)
        enr.status = 'approved'
        enr.save()
        time_from_str = format_date_time(enr.date, enr.time_from)
        time_from_tz = enr.order.klass.get_timezone()
        link = settings.FULL_URL + '/dashboard/learn/classes/'
        link2 = settings.FULL_URL + '/class/' + str(enr.order.klass.pk)
        # update when new sync link will be ready
        sync_link = settings.FULL_URL + '/ical'
        sign = get_message_sign(request, CompanyProfile)
        text = """Hi %s, 

%s with %s is rescheduled on: 
%s
Time zone: %s

%s

Sync to calendar here: %s
Check out the class here: %s


All the best, 

%s
%s 
%s 

%s
""" % (
        enr.order.user.first_name,
        enr.order.klass,
        enr.order.klass.teacher.first_name,
        time_from_str,
        time_from_tz,
        data.get('notice'),
        link,
        link2,
        enr.order.klass.teacher.first_name,
        enr.order.klass.teacher.phone or enr.order.klass.teacher.user.phone,
        enr.order.klass.teacher.email or enr.order.klass.teacher.user.email,
        sign,
)
        subject = 'Heads up! %s is rescheduled for %s' % (
            enr.order.klass,
            time_from_str,
        )
        if enr.order.user.phone:
            send_text(
                text,
                enr.order.user.phone,
            )

        email_list = [enr.order.user.email]
        send_mail_reply_to(
            subject,
            text,  # body
            settings.DEFAULT_FROM_EMAIL,
            email_list,
            fail_silently=True,
            reply_to=[enr.order.klass.teacher.email or enr.order.klass.teacher.user.email],
        )
        enr.order.update_reserved_lessons()
        return Response({
            'status': True,
            'enrollment': EnrSer(enr).data,
        })


class TeacherScheduleEnrollmentView(APIView):
    def post(self, request):
        data = request.data

        order = ClassLearner.objects.get(
            pk=data.get('orderId'),
            klass__teacher__user=request.user,
        )
        class_tz = pytz.timezone(order.klass.timezone)

        enr_objs = {}
        num = 0
        for x in PrivateEnroll.objects.filter(order=order.pk).values('date', 'time_from', 'status'):
            if not enr_objs.get(x['date']):
                enr_objs[x['date']] = {}
            enr_objs[x['date']][x['time_from']] = x
            if x['status'] != 'rejected':
                num += 1
        if num >= order.num_lessons:
            return Response({'status': False, 'overbooked': True})


        enr_data = {
            'order': order.pk,
            'date': data.get('selectedDate'),
            'time_from': data.get('timeFrom'),
            'time_to': data.get('timeTo'),
            'status': 'approved',
            # 'secret': key,
        }
        # if enr_objs.get(enr_data['date']) and enr_objs[enr_data['date']].get(enr_data['time_from']):
        #     # already exists
        #     continue

        x = datetime.strptime('%s %s' % (enr_data['date'], enr_data['time_from']), '%Y-%m-%d %H:%M')
        x = class_tz.localize(x)

        # if x <= datetime.now(class_tz):
        #     # no actions in past
        #     continue

        enr_data['time_from_gmt'] = x

        pes = PrivateEnrollSerializer(data=enr_data)
        pes.is_valid(raise_exception=True)
        enr = pes.save()

        time_from_str = format_date_time(enr.date, enr.time_from)
        time_from_tz = enr.order.klass.get_timezone()
        link = settings.FULL_URL + '/dashboard/learn/classes/'
        sign = get_message_sign(request, CompanyProfile)
        text = """Hi %s,

\"%s\" with %s is scheduled for %s %s.
%s
To reply, please text %s directly at %s. 

%s""" % (
        enr.order.user.first_name,
        enr.order.klass,
        enr.order.klass.teacher.first_name,
        time_from_str,
        time_from_tz,
        link,
        enr.order.klass.teacher.first_name,
        enr.order.klass.teacher.phone or enr.order.klass.teacher.user.phone,
        sign,
)
        subject = 'Heads up! %s is scheduled for %s %s' % (
            enr.order.klass,
            time_from_str,
            time_from_tz,
        )
        if enr.order.user.phone:
            send_text(
                text,
                enr.order.user.phone,
            )

        email_list = [enr.order.user.email]
        send_mail_reply_to(
            subject,
            text,  # body
            settings.DEFAULT_FROM_EMAIL,
            email_list,
            fail_silently=True,
            reply_to=[enr.order.klass.teacher.email or enr.order.klass.teacher.user.email],
        )
        enr.order.update_reserved_lessons()
        return Response({'status': True})


class RequestClassView(APIView):
    def post(self, request):
        data = request.data
        subject = 'Class Request'

        text = """email: %s
phone: %s
topic: %s""" % (
            data['email'],
            data['phone'],
            data['topic'],
        )

        email_list = ['alisacromer@gmail.com']
        send_mail(
            subject,
            text,  # body
            settings.DEFAULT_FROM_EMAIL,
            email_list,
            fail_silently=True,
        )

        return Response({'status': True})


class CancelEnrollmentView(generics.CreateAPIView):
    serializer_class = PrivateEnrollSerializer

    def post(self, request, pk):
        pe = PrivateEnroll.objects.get(
            pk=pk,
            order__user=request.user
        )
        status = False
        if pe.status == 'requested' or pe.status == 'approved':
            pe.status = 'rejected'
            pe.decline_reason = 'Declined by student'
            pe.save()
            status = True
            pe.order.update_reserved_lessons()
        return Response({'status': status})


class TeacherCancelPrivateEnrollmentView(generics.CreateAPIView):
    serializer_class = PrivateEnrollSerializer

    def post(self, request):
        teachers = Teacher.objects.filter(user=request.user)
        if request.user.is_company:
            teachers = teachers | Teacher.objects.filter(user__belongs_to=request.user.company.pk)
        
        pe = PrivateEnroll.objects.filter(
            pk__in=request.data['enrollment_ids'],
            order__klass__teacher__in=teachers,
        )
        affected_orders = set()
        for enr in pe:
            enr.status = 'rejected'
            enr.decline_reason = 'rescheduled by teacher'
            enr.save()
            enr.order.update_reserved_lessons()
            affected_orders.add(enr.order)
        for order in affected_orders:
            if request.data['message']:
                send_mail_reply_to(
                    'Reschedule notification.',  # subject
                    '%s. %s' % (
                        order.klass.name,
                        request.data['message'],
                    ),  # body
                    settings.DEFAULT_FROM_EMAIL,
                    [enr.order.user.email, ],
                    fail_silently=True,
                    reply_to=[order.klass.teacher.email or order.klass.teacher.user.email],
                )
        return Response({'status': True})


class VideoFormView(APIView):
    def post(self, request):
        data = request.data
        status = True

        Enr = GroupEnroll
        is_group = True
        if data['data']['isPrivate']:
            Enr = PrivateEnroll
            is_group = False

        enr = Enr.objects.get(pk=data['data']['id'], order__klass__teacher__user=request.user)

        if is_group:
            filter_dict = {s['email']: True for s in data['data']['students']}
            email_list = filter(lambda x: x in filter_dict, GroupEnroll.objects.filter(
                order__klass=enr.order.klass,
                date=enr.date,
                time_from=enr.time_from,
            ).values_list('order__user__email', flat=True))
        else:
            email_list = [enr.order.user.email]
        for email in email_list:
            text = """%s
Link for your class %s: %s
%s""" % (
                data['message'],
                data['data']['className'],
                data['url'],
                enr.order.klass.teacher.phone or enr.order.klass.teacher.user.phone,
            )
            try:
                send_mail_reply_to(
                    'Link for teachbeach class',  # subject
                    text,  # body
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=True,
                    reply_to=[enr.order.klass.teacher.email or enr.order.klass.teacher.user.email],
                )
            except SMTPDataError as e:
                return Response({'status': False, 'err': e.smtp_error})

        return Response({'status': status})


class SendOffersView(APIView):
    def post(self, request):
        enr_id = request.data['enrollment_id']
        is_private = request.data['is_private']
        if is_private:
            Enr = PrivateEnroll
        else:
            Enr = GroupEnroll
        enr = Enr.objects.get(pk=enr_id, order__klass__teacher__user=request.user)
        url = settings.FULL_URL + '/learners/new_enroll/%s/4/%s' % (
            enr.order.klass.pk,
            enr.order.pk,
        )

        congrats = "Congrats on completing %s class%s in %s." % (
            enr.order.num_lessons,
            'es' if enr.order.num_lessons > 1 else '',
            enr.order.klass
        )
        sign = get_message_sign(request, CompanyProfile)
        text = request.data['message'] or (f"Hi {enr.order.user.first_name}\n\n"
            f"{congrats}\n\n"
            f"You are on a roll! {enr.order.klass.teacher.first_name} invites you to keep learning. Enroll with one click {url}\n\n"
            f"{sign}\n\n")

        subj = f'Invitation from {enr.order.klass.teacher.first_name}'
        if enr.order.klass.teacher.user.is_company:
            subj = subj + ' @ ' + enr.order.klass.teacher.user.company.name
        try:
            send_mail_reply_to(
                subj,  # subject
                text,  # body
                settings.DEFAULT_FROM_EMAIL,
                [enr.order.user.email],
                fail_silently=True,
                reply_to=[enr.order.klass.teacher.email or enr.order.klass.teacher.user.email],
            )
        except SMTPDataError as e:
            return Response({'status': False, 'err': e.smtp_error})
        send_text(
            f"Teachbeach: {enr.order.klass.teacher.first_name} has invited you to keep learning {url}",
            enr.order.user.phone
        )

        return Response({'status': True})


class SendStudentEmailView(APIView):
    def post(self, request):
        order_id = request.data['order_id']
        message = request.data['message']

        order = ClassLearner.objects.get(
            pk=order_id,
            klass__teacher__user=request.user,
        )
        try:
            send_mail_reply_to(
                'Teachbeach Order',  # subject
                message,  # body
                settings.DEFAULT_FROM_EMAIL,
                [order.user.email],
                fail_silently=True,
                reply_to=[order.klass.teacher.email or order.klass.teacher.user.email],
            )
        except SMTPDataError as e:
            return Response({'status': False, 'err': e.smtp_error})

        return Response({'status': True})


class ICalView(APIView):
    def post(self, request):

        def next_weekday(d, weekday):
            days_ahead = weekday - (d.isoweekday() % 7)
            if days_ahead < 0: # Target day already happened this week
                days_ahead += 7
            return d + timedelta(days_ahead)

        cal = icalendar.Calendar()
        event = icalendar.Event()

        date_st = "2020-06-15 12:22"
        date_end = "2020-06-15 14:22"
        tz = 'US/Eastern'
        summary = 'Teachbeach Description'
        location = 'Address'

        # data = {
        #     'day_select_type': "weekly",
        #     'schedule_excluded': ["2020-08-26", "2020-08-27", "2020-09-06"],
        #     'start_date': "2020-08-20",
        #     'timezone': "EST",
        #     'until_date': None,
        #     'weekdays_schedule': [
        #         {'end': "08:45", 'start': "06:15", 'weekday': 0},
        #         # {'end': "08:45", 'start': "06:15", 'weekday': 0},
        #         # {'end': "08:45", 'start': "06:15", 'weekday': 3},
        #         # {'end': "08:45", 'start': "06:15", 'weekday': 2},
        #         {'end': "10:15", 'start': "06:25", 'weekday': 4},
        #     ],
        #     'summary': 'Teachbeach Description',
        #     'location': 'Address',
        # }
        data = request.data['schedule']

        date_st = data.get('start_date')
        date_end = None
        if data.get('until_date'):
            date_end = data.get('until_date')
        tz = data.get('timezone')

        short_tz = {
            'EST': 'US/Eastern',
            'PT': 'US/Pacific',
            'CST': 'US/Central',
            'MT': 'US/Mountain',
        }
        if tz in short_tz:
            tz = short_tz[tz]

        if date_st:
            start_date = datetime.strptime(date_st, '%Y-%m-%d')
        else:
            start_date = None
        summary = data.get('summary')
        description = data.get('description')
        location = data.get('location')

        tz = pytz.timezone(tz)
        # x = datetime.strptime(date_st, '%Y-%m-%d %H:%M')
        # x = tz.localize(x)
        # event.add('dtstart', x)

        # if date_end:
        #     x = datetime.strptime(date_end, '%Y-%m-%d %H:%M')
        #     x = tz.localize(x)
        #     event.add('dtend', x)

        if location:
            event['location'] = icalendar.vText(location)
        event['summary'] = summary
        event['name']= summary
        if description:
            event['description'] = description

        weekdays = ['SU', 'MO','TU','WE','TH','FR', 'SA']

        if data['day_select_type'] == 'monthly':
            for ws in data['schedule_dates']:
                ev = copy.deepcopy(event)

                if ws.get('UID'):
                    ev['uid'] = ws['UID'] + '@teachbeach.com'

                x = datetime.strptime('%s %s' % (ws['date'], ws['start']), '%Y-%m-%d %H:%M')
                x = tz.localize(x)
                ev.add('dtstart', x)

                x = datetime.strptime('%s %s' % (ws['date'], ws['end']), '%Y-%m-%d %H:%M')
                x = tz.localize(x)
                ev.add('dtend', x)

                cal.add_component(ev)

        if data['day_select_type'] == 'weekly':
            for ws in data['weekdays_schedule']:
                ev = copy.deepcopy(event)
                rec_start_day = next_weekday(start_date, ws['weekday'])
                rec_start_day = rec_start_day.strftime("%Y-%m-%d")

                for ex in data['schedule_excluded']:
                    x = datetime.strptime('%s %s' % (ex, ws['start']), '%Y-%m-%d %H:%M')
                    x = tz.localize(x)
                    ev.add('exdate', x)

                x = datetime.strptime('%s %s' % (rec_start_day, ws['start']), '%Y-%m-%d %H:%M')
                x = tz.localize(x)
                ev.add('dtstart', x)

                x = datetime.strptime('%s %s' % (rec_start_day, ws['end']), '%Y-%m-%d %H:%M')
                x = tz.localize(x)
                ev.add('dtend', x)

                ev.add('rrule', {'freq': 'weekly', 'byday': [weekdays[ws['weekday']]]})
                cal.add_component(ev)

        resp = cal.to_ical()

        return HttpResponse(resp, content_type='text/calendar')


class TeacherMessageView(APIView):
    def post(self, request):
        assert request.data['to']['entity'] == 'teacher'
        teacher = Teacher.objects.get(pk=request.data['to']['id'])
        tm = TeacherMessage(
            user_from=request.user,
            teacher_to=teacher,
            message=request.data.get('message'),
            allow_contact=request.data.get('allowOther'),
        )
        tm.save()
        email_to = teacher.email or teacher.user.email
        body = '%s (%s): %s' % (request.user.first_name, request.user.email, tm.message)
        try:
            send_mail_reply_to(
                'Teachbeach: Message',  # subject
                body,
                settings.DEFAULT_FROM_EMAIL,
                [email_to],
                fail_silently=True,
                reply_to=[request.user.email or settings.DEFAULT_FROM_EMAIL],
            )
        except SMTPDataError as e:
            return Response({'status': False, 'err': e.smtp_error})
        return Response({'status': True})


class AutoCompleteView(APIView):
    def get(self, request):
        q = request.GET.get('q')
        if not q:
            return Response({'res': []})
        res = {}
        cat = Category.objects.filter(name__icontains=q)
        res['categories'] = CategorySerializer(cat, many=True).data

        # all available subcategories
        classes = Class.objects.filter(is_deactivated=False)
        today = datetime.now().strftime("%Y-%m-%d")
        classes = classes.filter(
            Q(until_date='') |
            Q(until_date__isnull=True) |
            Q(until_date__gte=today)
        )
        classes = classes.exclude(Q(flexible_dates=False) & Q(is_private=False) & Q(start_date__lte=today) & Q(drop_in_rate__isnull=True))
        subcategories = classes.annotate(
            arr_els=Func(F('subcategories'), function='unnest')
        ).values_list('arr_els', flat=True).distinct()

        subc = SubCategory.objects.filter(name__icontains=q, pk__in=subcategories)
        res['subcategories'] = SubCategorySerializer(subc, many=True).data

        addresses = classes.filter(
            teaching_venue__icontains=q,
        ).values('teaching_venue').distinct()
        res['venues'] = addresses

        teachers = Teacher.objects.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
        res['teachers'] = [{'id': t.id, 'name': t.first_name+' '+t.last_name } for t in teachers]

        res['classes'] = [{'id': c.pk, 'name': c.private_className if c.is_private else c.name} for c in classes.filter(
            Q(name__icontains=q) | Q(private_className__icontains=q)
        )]
        return Response({'res': res})


class SendAddStudent(APIView):
    def post(self, request):
        type = request.data.get('type')
        email = request.data.get('email')
        emails = request.data.get('emails', [])
        name = request.data.get('name')
        phone = request.data.get('phone')
        class_id = request.data.get('class_id')
        msg = request.data.get('message', '')
        filter = request.data.get('filter', None)

        if request.user.is_company:
            klass = Class.objects.get(
                Q(pk=class_id), Q(teacher__user=request.user) | Q(teacher__user__belongs_to=request.user.company.pk)
            )
        else:
            klass = Class.objects.get(
                pk=class_id, teacher__user=request.user
            )

        def matcher(match):
            # print(match, flush=True)
            return f"/3/?name={urllib.parse.quote(name)}&phone={urllib.parse.quote(phone)}&email={email}" if type == 'new' else f"/4/?login"

        def add_single(name, email, phone, custom_message=None):
            add = AddStudent(
                name=name,
                phone=phone,
                email=email,
                class_id=klass.pk
            )
            add.save()

            if custom_message:
                message = custom_message
            else:
                link = f"https://teachbeach.com/learners/{class_id}/3/?name={urllib.parse.quote(name)}&phone={urllib.parse.quote(phone)}&email={email}"
                message = re.sub('/3/\?name=([^&]+|)&phone=([^&]+|)&email=(\S+|)', matcher, msg) \
                          or 'You have been invited to the class: %s. Please register to complete order: %s' % (
                    klass.name,
                    link,
                )
            subj = 'Invitation from %s' % (request.user.first_name)
            if klass.teacher.user.is_company:
                subj = subj + ' @ ' + klass.teacher.user.company.name
            send_mail_reply_to(
                subj,  # subject
                message,  # body
                settings.DEFAULT_FROM_EMAIL,
                [email, 'alisa@teachbeach.com',],
                fail_silently=True,
                reply_to=[klass.teacher.email or klass.teacher.user.email],
            )
            subj = 'Copy: Invitation from %s' % (request.user.first_name)
            if klass.teacher.user.is_company:
                subj = subj + ' @ ' + klass.teacher.user.company.name
            if request.data.get('copyMe'):
                send_mail(
                    subj,  # subject
                    message,  # body
                    settings.DEFAULT_FROM_EMAIL,
                    [klass.teacher.email or klass.teacher.user.email],
                    fail_silently=True,
                )

            if phone:
                send_text(
                    message,
                    phone
                )

        if email:
            if type == 'registered':
                try:
                    user = User.objects.filter(email=email)[0]
                    name = user.first_name
                    phone = user.phone
                    add_single(name=name, email=email, phone=phone)
                except User.DoesNotExist:
                    return Response({'success': False, 'error_message': 'User with such email does not exist'})
            else:
                add_single(name=name, email=email, phone=phone)
        elif filter and not len(emails):
            teachers = Teacher.objects.filter(user=request.user)

            pr = list(PrivateEnroll.objects.filter(
                order__klass__teacher__in=teachers,
            ))

            gr = list(GroupEnroll.objects.filter(
                order__klass__teacher__in=teachers,
            ))
            all_users = [x.order.user.pk for x in pr]
            all_users += [x.order.user.pk for x in gr]
            students = MembershipStudent.objects.filter(membership__owner_user__pk=request.user.pk, is_active=True)
            member_ids = [s.student_id for s in students]
            teacher_classes = Class.objects.filter(teacher__user=request.user)

            customers = ClassLearner.objects.filter(
                klass__teacher__in=teachers,
                status='succeeded',
            ).values('user')

            if filter == 'all':
                users = User.objects.filter(Q(pk__in=all_users) | Q(class_id__in=teacher_classes))
            elif filter == 'members':
                users = User.objects.filter(pk__in=member_ids)
            elif filter == 'customers':
                users = User.objects.filter(Q(pk__in=[y['user'] for y in customers] + member_ids))
            elif filter == 'registered':
                users = User.objects.filter(class_id__in=teacher_classes)
            elif filter == 'unregistered':
                users = User.objects.filter(managed_by__contains=[request.user.pk])
            elif filter == 'prospects':
                users = User.objects.filter(Q(managed_by__contains=[request.user.pk]) | Q(class_id__in=teacher_classes))
            elif filter == 'students':
                users = User.objects.filter(Q(pk__in=all_users))
            else:
                users = User.objects.filter(Q(class_id__in=teacher_classes)).exclude(pk__in=all_users)
            for u in users:
                try:
                    add_single(name=u.first_name, email=u.email, phone=u.phone, custom_message=msg)
                except User.DoesNotExist:
                    pass
        else:
            for email in emails:
                try:
                    user = User.objects.filter(email=email).first()
                    name = user.first_name
                    phone = user.phone
                    add_single(name=name, email=email, phone=phone, custom_message=msg)
                except User.DoesNotExist:
                    pass
        return Response({'success': True})


class TeacherStudentsEmail(APIView):
    permissions = [permissions.IsAuthenticated, ]

    def post(self, request):
        text = request.data.get('text')
        subject = request.data.get('subject')
        if not text:
            return Response({'success': False, 'error': 'Empty text'}, status=status.HTTP_400_BAD_REQUEST)
        
        instructors = [request.user.pk]
        if request.user.is_company:
            instructors = instructors + [x.pk for x in User.objects.filter(belongs_to=request.user.company.pk)]
        teachers = Teacher.objects.filter(user__in=instructors)

        pr = list(PrivateEnroll.objects.filter(
            order__klass__teacher__in=teachers,
        ))

        gr = list(GroupEnroll.objects.filter(
            order__klass__teacher__in=teachers,
        ))
        all_users = [x.order.user.pk for x in pr]
        all_users += [x.order.user.pk for x in gr]
        orders = [x.order.pk for x in pr]
        orders += [x.order.pk for x in gr]
        orders = ClassLearner.objects.filter(pk__in=orders)
        classes = [c.pk for c in Class.objects.filter(teacher__in=teachers)]
        students = MembershipStudent.objects.filter(membership__owner_user__pk=request.user.pk, is_active=True)
        member_ids = [s.student_id for s in students]

        customers = ClassLearner.objects.filter(
            klass__teacher__in=teachers,
            status='succeeded',
        ).values('user')

        teacher_classes = Class.objects.filter(teacher__in=teachers)
        if request.data.get('filter') == 'all':
            users = User.objects.filter(Q(pk__in=all_users)|Q(class_id__in=teacher_classes))
        elif request.data.get('filter') == 'members':
            users = User.objects.filter(pk__in=member_ids)
        elif request.data.get('filter') == 'customers':
            users = User.objects.filter(Q(pk__in=[y['user'] for y in customers]+member_ids))
        elif request.data.get('filter') == 'registered':
            users = User.objects.filter(class_id__in=classes)
        elif request.data.get('filter') == 'unregistered':
            users = User.objects.filter(managed_by__contains=[request.user.pk])
        elif request.data.get('filter') == 'prospects':
            users = User.objects.filter(Q(managed_by__contains=[request.user.pk])|Q(class_id__in=classes))
        elif request.data.get('filter') == 'students':
            users = User.objects.filter(Q(pk__in=all_users))
        elif request.data.get('filter') == 'selected' and request.data.get('students'):
            student_ids = filter(lambda x: 't' not in str(x), set(request.data.get('students')))
            teacher_ids = [str(x).replace('t', '') for x in filter(lambda x: 't' in str(x), set(request.data.get('students')))]
            users = User.objects.filter(Q(pk__in=all_users + instructors)|Q(class_id__in=teacher_classes)|Q(managed_by__contains=[request.user.pk])).filter(pk__in=student_ids)
            if len(teacher_ids):
                users = [u for u in users] + [t for t in Teacher.objects.filter(pk__in=teachers).filter(pk__in=teacher_ids).exclude(email__isnull=True).exclude(email__exact='')]
        else:
            users = User.objects.filter(Q(class_id__in=teacher_classes)).exclude(pk__in=all_users)
        #body = f'Message from {request.user.company.name if request.user.is_company else request.user.first_name}: \n'
        body = text
        # body += '\n '
        for u in users:
            send_mail_reply_to(
                subject or 'Teachbeach Message',  # subject
                strip_tags(body),  # body
                settings.DEFAULT_FROM_EMAIL,
                [u.email, ],
                fail_silently=True,
                reply_to=[request.user.email or settings.DEFAULT_FROM_EMAIL],
                html_message=body,
            )
            if request.data.get('copyMe'):
                send_mail(
                    subject or 'Teachbeach Message',  # subject
                    strip_tags(body),  # body
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=True,
                    html_message=body,
                )
        return Response({'success': True})


class TeacherBulkRescheduleView(APIView):
    def post(self, request):
        teachers = Teacher.objects.filter(user=request.user)
        if request.user.is_company:
            teachers = teachers | Teacher.objects.filter(user__belongs_to=request.user.company.pk)
        ge = GroupEnroll.objects.filter(
            pk__in=request.data['enrollment_ids'],
            order__klass__teacher__in=teachers,
            order__klass=request.data['class_id']
        )
        assert ge.count() == len(request.data['enrollment_ids'])

        c = Class.objects.get(
            pk=request.data['class_id'],
            teacher__in=teachers,
        )
        class_tz = pytz.timezone(c.timezone)

        x = datetime.strptime('%s %s' % (request.data['date_to'], request.data['time_start']), '%Y-%m-%d %H:%M')
        x = class_tz.localize(x)

        for enr in ge:
            enr.date = request.data['date_to']
            enr.time_from = request.data['time_start']
            enr.time_to = request.data['time_end']
            enr.time_from_gmt = x
            enr.save()
            # notification
            send_mail_reply_to(
                'Reschedule notification.',  # subject
                '%s. %s' % (
                    c.name,
                    request.data['message'],
                ),  # body
                settings.DEFAULT_FROM_EMAIL,
                [enr.order.user.email, ],
                fail_silently=True,
                reply_to=[enr.order.klass.teacher.email or enr.order.klass.teacher.user.email],
            )
        new_schd = filter(lambda x: x['date'] != request.data['date_from'], c.schedule_dates)
        new_schd = list(new_schd)
        new_schd.append({
            'date': request.data['date_to'],
            'start': request.data['time_start'],
            'end': request.data['time_end'],
        })
        c.schedule_dates = new_schd
        c.save()

        return Response({'success': True, 'schedule_dates': c.schedule_dates})


class TeacherSignInStudentView(APIView):
    def post(self, request):
        data = request.data
        teachers = Teacher.objects.filter(user=resquest.user)
        if request.user.is_company:
            teachers = teachers | Teacher.objects.filter(user__belongs_to=request.user.company.pk)
        order = ClassLearner.objects.get(
            pk=data['order_id'],
            klass__teacher__in=teachers,
        )
        if order.reserved_lessons >= order.num_lessons:
            return Response({'success': False, 'message': 'No classes left for order.'})
        klass = order.klass
        class_tz = pytz.timezone(order.klass.timezone)

        found_date = None
        #enr = None
        if klass.is_private:
            if order.is_subscription and order.status != 'active':
                return Response({
                    'status': False,
                    'message': order.status,
                })
            enr_objs = {}
            num = 0
            for x in PrivateEnroll.objects.filter(order=order.pk).values('date', 'time_from', 'status'):
                if not enr_objs.get(x['date']):
                    enr_objs[x['date']] = {}
                enr_objs[x['date']][x['time_from']] = x
                if x['status'] != 'rejected':
                    num += 1

            key = str(uuid.uuid1())

            x = datetime.strptime('%s %s' % (data['date'], data['time']), '%Y-%m-%d %H:%M')
            time_to = (x + timedelta(minutes=order.data['package']['lessonLength']['value'])).strftime('%H:%M')
            x = class_tz.localize(x)

            enr_data = {
                'order': order.pk,
                'date': data['date'],
                'time_from': data['time'],
                'time_to': time_to,
                'secret': key,
                'status': 'approved',
            }
            if enr_objs.get(enr_data['date']) and enr_objs[enr_data['date']].get(enr_data['time_from']):
                # already exists
                return Response({
                    'status': False,
                    'message': 'Time slot already in use',
                })

            if x <= datetime.now(class_tz):
                # no actions in past
                return Response({
                    'status': False,
                    'message': "Can't sign in in the past",
                })

            if order.num_lessons <= num:
                return Response({
                    'status': False,
                    'message': "Overbooked",
                })
            num += 1
            enr_data['time_from_gmt'] = x

            es = PrivateEnrollSerializer(data=enr_data)
            es.is_valid(raise_exception=True)
            enr = es.save()
        else:
            if klass.schedule_dates:
                for x in klass.schedule_dates:
                    if x['date'] == data['date']:
                        found_date = x
                        break

            if not found_date:
                return Response({'success': False, 'message': 'Invalid date'})

            x = datetime.strptime('%s %s' % (found_date['date'], found_date['start']), '%Y-%m-%d %H:%M')
            x = class_tz.localize(x)

            enr_data = {
                'order': data['order_id'],
                'date': found_date['date'],
                'time_from': found_date['start'],
                'time_to': found_date['end'],
                'time_from_gmt': x,
            }
            es = GroupEnrollSerializer(data=enr_data)
            es.is_valid(raise_exception=True)
            enr = es.save()

        time_from_str = format_date_time(enr.date, enr.time_from)
        time_from_tz = enr.order.klass.get_timezone()
        link = settings.FULL_URL + '/dashboard/learn/classes/'
        sign = get_message_sign(request, CompanyProfile)
        text = """Hi %s,

\"%s\" with %s is scheduled for %s %s.
%s
To reply, please text %s directly at %s. 

%s""" % (
        enr.order.user.first_name,
        enr.order.klass,
        enr.order.klass.teacher.first_name,
        time_from_str,
        time_from_tz,
        link,
        enr.order.klass.teacher.first_name,
        enr.order.klass.teacher.phone or enr.order.klass.teacher.user.phone,
        sign,
)
        subject = 'Heads up! %s is scheduled for %s %s' % (
            enr.order.klass,
            time_from_str,
            time_from_tz,
        )
        if enr.order.user.phone:
            send_text(
                text,
                enr.order.user.phone,
            )

        email_list = [enr.order.user.email]
        send_mail_reply_to(
            subject,
            text,  # body
            settings.DEFAULT_FROM_EMAIL,
            email_list,
            fail_silently=True,
            reply_to=[enr.order.klass.teacher.email or enr.order.klass.teacher.user.email],
        )

        order.update_reserved_lessons()

        return Response({'success': True, 'enr': es.data})


class UserSettingsView(APIView):
    def get(self, request):
        us, _ = UserSettings.objects.get_or_create(user=request.user)
        settings = UserSettingsSerializer(us).data
        return Response({'settings': settings['settings']})

    def post(self, request):
        us, _ = UserSettings.objects.get_or_create(user=request.user)
        us.settings = request.data.get('settings', {})
        us.save()
        settings = UserSettingsSerializer(us).data
        return Response({'success': True, 'settings': settings['settings']})


class TeacherDashboardPreloadView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=401)
        result = {
            'upcoming': False,
            'previous': False,
        }
        teachers = Teacher.objects.filter(user=request.user)
        if not teachers:
            return Response(result)

        today = datetime.now()

        upcoming = PrivateEnroll.objects.filter(
            order__klass__teacher__in=teachers,
            order__klass__deleted_at=None,
            status='approved',
            time_from_gmt__gte=today,
        ).first()
        if not upcoming:
            upcoming = GroupEnroll.objects.filter(
                order__klass__teacher__in=teachers,
                order__klass__deleted_at=None,
                status='approved',
                time_from_gmt__gte=today,
            ).first()

        previous = PrivateEnroll.objects.filter(
            order__klass__teacher__in=teachers,
            order__klass__deleted_at=None,
            status='approved',
            time_from_gmt__lte=today,
        ).first()
        if not previous:
            previous = GroupEnroll.objects.filter(
                order__klass__teacher__in=teachers,
                order__klass__deleted_at=None,
                status='approved',
                time_from_gmt__lte=today,
            ).first()

        result['upcoming'] = True if upcoming else False
        result['previous'] = True if previous else False

        return Response(result)


class DeleteStudentView(APIView):
    def post(self, request):
        student_ids = request.data.get('ids', [])
        for student_id in student_ids:
            DeletedStudent.objects.get_or_create(user=request.user, student_id=student_id)
        return Response({'success': True})


class AddManagedStudent(APIView):
    def post(self, request):
        user_data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone'),
            'source': request.data.get('source'),
            'notes': request.data.get('notes'),
            'managed_by': [request.user.pk],
            'timezone': request.user.timezone,
        }
        serializer = ManagedUserSerializer(data=user_data)
        serializer.is_valid(True)
        user_data = serializer.validated_data
        user = get_user_model().objects.create_user(user_data['email'].lower(), **user_data)
        return Response({'success': True, 'student': UserShortSerializer(user).data})


class UpdateManagedStudent(APIView):
    def post(self, request):
        try:
            user = get_user_model().objects.get(pk=request.data.get('id'))
        except User.DoesNotExist:
            return Response({'success': False, 'error_message': 'User not found'})
        if request.user.pk not in user.managed_by:
            return Response({'success': False, 'error_message': 'Student not managed by current user'})
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.phone = request.data.get('phone')
        user.source = request.data.get('source')
        user.notes = request.data.get('notes')
        user.notes2 = request.data.get('notes2')
        user.save()
        return Response({'success': True, 'student': UserShortSerializer(user).data})

class ExternalCalendarView(APIView):
    def get(self, request):
        events = ExternalCalendar.objects.filter(user=request.user).values('provider_type', 'provider_id', 'data')
        return Response({'success': True, 'calendars': events})

    def post(self, request):
        events, _ = ExternalCalendar.objects.get_or_create(
            user=request.user,
            provider_type=request.data.get('provider_type'),
            provider_id=request.data.get('provider_id'),
        )
        events.data = request.data.get('events')
        events.save()
        return Response({'success': True})


class UploadStudents(APIView):
    def post(self, request):
        _, encoded = request.data.get('url').split(';base64,')
        f = StringIO(str(base64.b64decode(encoded)).replace('\\n', '\n').replace('\\r', '\r'))
        reader = csv.reader(f)
        next(reader, None)
        success = 0
        fail = 0
        membership = Membership.objects.get(owner_user=request.user)
        for row in reader:
            try:
                user_data = {
                    'first_name': row[0],
                    'last_name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'source': row[4] if len(row) > 4 else None,
                    'notes': row[5] if len(row) > 5 else None,
                    'notes2': row[6] if len(row) > 6 else None,
                    'managed_by': [request.user.pk],
                    'timezone': request.user.timezone,
                }
                serializer = ManagedUserSerializer(data=user_data)
                serializer.is_valid(True)
                user_data = serializer.validated_data
                user = get_user_model().objects.create_user(user_data['email'].lower(), **user_data)
                success = success + 1
                if request.GET.get('type') == 'members':
                    MembershipStudent.objects.create(
                        student=user,
                        membership=membership,
                        currency=membership.currency,
                        weekly_rate=membership.weekly_rate,
                        monthly_rate=membership.monthly_rate,
                        yearly_rate=membership.yearly_rate,
                        is_permanent=True,
                        amount=0,
                        amount_full=0,
                    )
            except:
                fail = fail + 1
        f.close()
        return Response({
            'success': True,
            'added': success,
            'skipped': fail,
        })


class MembershipView(APIView):
    def get(self, request):
        try:
            membership = Membership.objects.get(owner_user=request.user)
            membership = MembershipSerializer(membership).data
        except Membership.DoesNotExist:
            membership = None
        return Response({'success': True, 'membership': membership})

    def post(self, request):
        data = request.data
        membership, _ = Membership.objects.get_or_create(
            owner_user=request.user,
        )
        membership.currency = request.data.get('currency')
        membership.weekly_rate = decimal.Decimal(request.data.get('weekly_rate'))
        membership.monthly_rate = decimal.Decimal(request.data.get('monthly_rate'))
        membership.yearly_rate = decimal.Decimal(request.data.get('yearly_rate'))
        membership.description = request.data.get('description')
        membership.name = request.data.get('name')
        membership.isDirectoryEnabled = request.data.get('isDirectoryEnabled')
        membership.isDMEnabled = request.data.get('isDMEnabled')
        membership.isChatEnabled = request.data.get('isChatEnabled')
        membership.isUploadAllowed = request.data.get('isUploadAllowed')
        membership.isUploadRequired = request.data.get('isUploadRequired')
        membership.isAboutAllowed = request.data.get('isAboutAllowed')
        membership.isAboutRequired = request.data.get('isAboutRequired')
        membership.isTitleAllowed = request.data.get('isTitleAllowed')
        membership.isTitleRequired = request.data.get('isTitleRequired')
        membership.isCityAllowed = request.data.get('isCityAllowed')
        membership.isCityRequired = request.data.get('isCityRequired')
        membership.isProjectsAllowed = request.data.get('isProjectsAllowed')
        membership.isProjectsRequired = request.data.get('isProjectsRequired')
        membership.isSocialAllowed = request.data.get('isSocialAllowed')
        membership.isSocialRequired = request.data.get('isSocialRequired')
        membership.isPhoneAllowed = request.data.get('isPhoneAllowed')
        membership.isPhoneRequired = request.data.get('isPhoneRequired')
        membership.isEmailAllowed = request.data.get('isEmailAllowed')
        membership.isEmailRequired = request.data.get('isEmailRequired')
        membership.isDocumentAllowed = request.data.get('isDocumentAllowed')
        membership.isDocumentRequired = request.data.get('isDocumentRequired')
        membership.customInterestsField = request.data.get('customInterestsField')
        membership.customSkillsField = request.data.get('customSkillsField')
        membership.customLevelsField = request.data.get('customLevelsField')
        membership.save()
        if data.get('picture') and data['picture']['uploadPhoto']['imageUrl'] and data['picture']['uploadPhoto']['imageUrl'].startswith('data:'):
            imgstr = data['picture']['uploadPhoto']['imageUrl']
            imgname = data['picture']['uploadPhoto']['imageName']
            _, imgstr = imgstr.split(';base64,')
            name = '%s-%s-%s' % (membership.id, uuid.uuid1(), imgname)
            fdata = ContentFile(base64.b64decode(imgstr), name=name)
            membership.media = fdata
            membership.save()
            membership.save_thumbnail()

        return Response({'success': True, 'membership': MembershipSerializer(membership).data})


class MembershipByIdView(generics.RetrieveAPIView):
    def get(self, request, pk):
        membership = None
        try:
            membership = Membership.objects.get(pk=pk)
            membership = MembershipSerializer(membership).data
        except Membership.DoesNotExist:
            Response({'success': False})
        return Response({'success': True, 'membership': membership})


class StudentMembershipView(APIView):
    def get(self, request):
        memberships = MembershipStudent.objects.filter(student__pk=request.user.pk, is_active=True)
        membershipSettings = Membership.objects.filter(pk__in=[m.membership.pk for m in memberships])
        return Response({
            'success': True, 
            'memberships': MembershipStudentSerializer(memberships, many=True).data,
            'membershipSettings': MembershipSerializer(membershipSettings, many=True).data,
        })

    def post(self, request):
        membership = MembershipStudent.objects.get(student__pk=request.user.pk, pk=request.data.get('student_membership_id'))
        membershipSetting = Membership.objects.get(pk=membership.membership.pk)
        if membershipSetting.isAboutRequired and not request.data.get('description'):
            return Response({
                'success': False,
                'field': 'description',
                'error': 'Description is required field',
            })
        if membershipSetting.isTitleRequired and not request.data.get('title'):
            return Response({
                'success': False,
                'field': 'title',
                'error': 'Title is required field',
            })
        if membershipSetting.isCityRequired and not request.data.get('city'):
            return Response({
                'success': False,
                'field': 'city',
                'error': 'City is required field',
            })
        if membershipSetting.isProjectsRequired and not request.data.get('website'):
            return Response({
                'success': False,
                'field': 'website',
                'error': 'Website is required field',
            })
        if membershipSetting.isSocialRequired and not request.data.get('social'):
            return Response({
                'success': False,
                'field': 'social',
                'error': 'Social is required field',
            })
        if membershipSetting.isPhoneRequired and not request.data.get('phone'):
            return Response({
                'success': False,
                'field': 'phone',
                'error': 'Phone is required field',
            })
        if membershipSetting.isEmailRequired and not request.data.get('email'):
            return Response({
                'success': False,
                'field': 'email',
                'error': 'Email is required field',
            })
        if membershipSetting.isDocumentRequired and not request.data.get('document'):
            return Response({
                'success': False,
                'field': 'document',
                'error': 'Document is required field',
            })
        request.user.first_name = request.data.get('firstName')
        request.user.last_name = request.data.get('lastName')
        if membershipSetting.isEmailAllowed:
            request.user.email = request.data.get('email')
        if membershipSetting.isPhoneAllowed:
            request.user.phone = request.data.get('phone')
        request.user.save()
        if membershipSetting.isAboutAllowed:
            membership.description = request.data.get('description')
        if membershipSetting.isTitleAllowed:
            membership.title = request.data.get('title')
        if membershipSetting.isCityAllowed:
            membership.city = request.data.get('city')
        if membershipSetting.isProjectsAllowed:
            membership.website = request.data.get('website')
        if membershipSetting.isSocialAllowed:
            membership.social = request.data.get('social')
        if membershipSetting.isDocumentAllowed:
            membership.document = request.data.get('document')
        membership.level = request.data.get('level')
        membership.skill = request.data.get('skill')
        membership.interest = request.data.get('interest')
        membership.save()
        return Response({
            'success': True,
            'data': MembershipStudentSerializer(membership).data,
        })

    def delete(self, request):
        membership = Membership.objects.get(pk=request.data.get('id'))
        #TODO: process stripe stuff
        membership.students.remove(request.user)
        return Response({'success': True})


class MembershipsListView(APIView):
    def get(self, request):
        try:
            memberships = Membership.objects.filter(deactivated_at=None)
            memberships = MembershipSerializer(memberships, many=True).data
        except Membership.DoesNotExist:
            memberships = []
        return Response({'memberships': memberships})


class ClassMembershipView(generics.RetrieveAPIView):
    def get(self, request, pk):
        membership = None
        try:
            klass = Class.objects.get(pk=pk)
            try:
                membership = MembershipSerializer(klass.teacher.user.membership).data
            except Membership.DoesNotExist:
                if klass.teacher.user.belongs_to:
                    company = CompanyProfile.objects.get(pk=klass.teacher.user.belongs_to)
                    membership = MembershipSerializer(company.user.membership).data
        except Class.DoesNotExist:
            Response(None)
        return Response({'success': True, 'membership': membership})


class ClassTeacherView(generics.RetrieveAPIView):
    def get(self, request, pk):
        teacher = None
        try:
            klass = Class.objects.get(pk=pk)
            teacher = TeacherSerializer(klass.teacher).data
        except Class.DoesNotExist:
            Response(None)
        return Response({'success': True, 'teacher': teacher})


class CompanyTeacherRequest(APIView):
    def post(self, request):
        cp = CompanyProfile.objects.get(pk=request.data.get('company_id'))
        user_data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone'),
            'managed_by': [cp.user.pk],
            'timezone': request.data.get('timezone'),
        }
        serializer = ManagedUserSerializer(data=user_data)
        serializer.is_valid(True)
        user_data = serializer.validated_data
        user = get_user_model().objects.create_user(user_data['email'].lower(), **user_data)
        send_mail_reply_to(
            'Instructor application',  # subject
            """New Instructor request.

Name: %s
Areas of expertise: %s
Background: %s
Email: %s
Phone: %s""" % (
                request.data.get('name'),
                request.data.get('areas'),
                request.data.get('background'),
                request.data.get('email'),
                request.data.get('phone'),
            ),  # body
            settings.DEFAULT_FROM_EMAIL,
            [cp.user.email, ],
            fail_silently=True,
            reply_to=[user.email],
        )
        return Response({'success': True})


class CompanyInstructorsView(generics.RetrieveAPIView):
    def get(self, request):
        data = request.data
        if request.user.is_company:
            users = User.objects.filter(belongs_to=request.user.company.pk)
        else:
            return Response([])
        return Response(UserShortSerializer(users, many=True).data)


@method_decorator(csrf_exempt, name='dispatch')
class VueEditorUploadFileView(View):
    parser_classes = (MultiPartParser, FormParser, )

    def post(self, request, format=None, *args, **kwargs):
        region = os.environ['AWS_REGION']
        key = os.environ['AWS_ACCESS_KEY_ID']
        secret = os.environ['AWS_SECRET_ACCESS_KEY']
        bucket = os.environ['AWS_S3_BUCKET']
        final_filename = str(uuid.uuid4()) + '.' + request.FILES['file'].name.split('.')[-1] 
        s3_client = boto3.client('s3', region_name=region, aws_access_key_id=key, aws_secret_access_key=secret)
        try:
            response = s3_client.upload_fileobj(request.FILES['file'], bucket, final_filename)
            return HttpResponse('https://' + bucket + '.s3.amazonaws.com/' + final_filename)
        except ClientError as e:
            return HttpResponse('upload error')


class FacebookSignUp(GenericAPIView):
    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        """

        POST with "auth_token"

        Send an access token as from facebook to get user information

        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        print('////')
        login(request, User.objects.get(username=data['username']))
        return Response(data, status=status.HTTP_200_OK)


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """

        POST with "auth_token"

        Send an idtoken as from google to get user information

        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        login(request, User.objects.get(username=data['username']))
        return Response(data, status=status.HTTP_200_OK)


class DiscussionSetupView(APIView):
    serializer_class = DiscussionSetupserializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        if data['is_community']:
            post = data['community_post']
            d = Discussion()
            d.type = "C"
            d.user = request.user
            d.title = post['description']
            if request.FILES.get("community_thumbnail", None):
                d.thumbnail = request.FILES['community_thumbnail']
            d.save()
            d.users.add(request.user)
            # COMMENT
            c = Comment.objects.create(
                user=request.user, 
                discussion=d,
                top_comment=True,
                content=post['description']   
            )
            # ADD PARTICIPANT
            if post['participants'] == 'members':
                d.users.add(
                    *MembershipStudent.objects.filter(
                        membership__owner_user=request.user,
                        status='active'
                    ).values('student')
                )
                print(d.users.all())

        elif data['is_topic']:
            pass
        elif data['is_event']:
            pass

        return Response({
            "detail": "Discussion Created.",
            "discussion_id": d.id
        }, status=status.HTTP_201_CREATED)


class DiscussionAllListView(APIView):
    serializer_class = DiscussionListSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(
            self.serializer_class(
                Discussion.objects.all(),
                many=True
            ).data,
            status=status.HTTP_200_OK
        )


class DiscussionDetailView(APIView):
    serializer_class = DiscussionDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            d = Discussion.objects.get(id=pk)
            allowed = request.user in d.users.all()
        else:
            d_filter =  Discussion.objects.filter(
                users__in=[request.user]
            )
            d = d_filter.last() if d_filter.exists() else ""
            allowed = True if d_filter.exists() else False

        if allowed:
            return Response(
                self.serializer_class(d).data,
                status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "No Description available for you."}, 
                status.HTTP_204_NO_CONTENT
            )


class DiscussionCommentView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, pk):
        serializer = self.serializer_class(
            Comment.objects.filter(
                discussion__id=pk, 
                top_comment=False,
                is_reply=False
            ), many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
