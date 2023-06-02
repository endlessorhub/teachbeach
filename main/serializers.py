from django.db.models import Sum
from rest_framework import serializers
from datetime import datetime

from .models import (
    Teacher, Venue, Class, ClassMedia,
    Category, SubCategory, ClassLearner,
    GlobalPackage, PrivateEnroll, GroupEnroll,
    Message, DraftClass, CompanyProfile,
    Newsletter, BoostMembership, EmailBoost,
    Event, MetaTag, UserSettings, Membership, MembershipStudent,
)
from . import facebook
from . import google
from .register import register_social_user
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from drf_extra_fields.fields import Base64ImageField
from django.db.models import Q
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    company_profile = serializers.SerializerMethodField()
    memberships = serializers.SerializerMethodField()
    membership = serializers.SerializerMethodField(required=False)

    def validate_email(self, value):
        try:
            get_user_model().objects.get(username__iexact=value)
        except:
            return value.lower()
        raise serializers.ValidationError("User with this email already exists")

    def get_company_profile(self, instance):
        if instance.belongs_to:
            company = CompanyProfile.objects.get(pk=instance.belongs_to)
            try:
                return CompanyProfileSerializer(company).data
            except ObjectDoesNotExist:
                pass
            return None
        try:
            if instance.is_company and instance.company:
                return CompanyProfileSerializer(instance.company).data
        except ObjectDoesNotExist:
            pass
        return None

    def get_memberships(self, instance):
        try:
            student_memberships = MembershipStudent.objects.filter(student=instance)
            return MembershipStudentSerializer(student_memberships, many=True).data
        except ObjectDoesNotExist:
            pass
        return []

    def get_membership(self, instance):
        if instance.belongs_to:
            company = CompanyProfile.objects.get(pk=instance.belongs_to)
            try:
                return company.user.membership.id
            except ObjectDoesNotExist:
                pass
            return None
        try:
            return instance.membership.pk
        except ObjectDoesNotExist:
            pass
        return None

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def create(self, validated_data):
        user = get_user_model().objects.create_user(validated_data['email'], **validated_data)
        return user

    class Meta:
        model = get_user_model()
        fields = ('id', 'password', 'first_name', 'last_name', 'email', 'phone', 'is_company', 'company_profile', 'timezone', 'lat', 'lng', 'tz_address', 'class_id', 'memberships', 'membership', 'belongs_to', 'source', 'notes')


class ManagedUserSerializer(UserSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'timezone', 'managed_by', 'source', 'notes', 'notes2')


class UserFutureClassesSerializer(UserSerializer):
    classes = serializers.SerializerMethodField()

    def get_classes(self, instance):

        today = datetime.now().strftime("%Y-%m-%d")

        pr = PrivateEnroll.objects.filter(
            order__user=instance,
            date__gte=today,
        ).values_list('order__klass__pk', flat=True).distinct()

        gr = GroupEnroll.objects.filter(
            order__user=instance,
            date__gte=today,
        ).values_list('order__klass__pk', flat=True).distinct()

        future_classes = list(pr) + list(gr)

        c = Class.objects.filter(
            pk__in=future_classes,
        )

        return ClassShortSerializer(c, many=True).data

    class Meta:
        model = get_user_model()
        fields = ('id', 'classes', 'first_name', 'last_name', 'email', 'phone', 'is_company', 'company_profile')


class UserAllClassesSerializer(UserSerializer):
    classes = serializers.SerializerMethodField()

    def get_classes(self, instance):

        pr = PrivateEnroll.objects.filter(
            order__user=instance,
        ).values_list('order__klass__pk', flat=True).distinct()

        gr = GroupEnroll.objects.filter(
            order__user=instance,
        ).values_list('order__klass__pk', flat=True).distinct()

        all_classes = list(pr) + list(gr)

        c = Class.objects.filter(
            pk__in=all_classes,
        )

        return ClassShortSerializer(c, many=True).data

    class Meta:
        model = get_user_model()
        fields = ('id', 'classes', 'first_name', 'last_name', 'email', 'phone', 'is_company', 'company_profile', 'source', 'notes', 'notes2', 'date_joined', 'managed_by', 'memberships')


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'is_company', 'timezone', 'membership', 'source', 'notes', 'notes2', 'date_joined', 'managed_by')


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class TeacherShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('description', 'media', 'id', 'areas_of_specialty', 'first_name', 'last_name', 'phone', 'email')


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    group_count = serializers.SerializerMethodField()
    private_count = serializers.SerializerMethodField()

    def get_group_count(self, instance):
        return Class.objects.filter(teacher=instance, is_private=False).count()

    def get_private_count(self, instance):
        return Class.objects.filter(teacher=instance, is_private=True).count()

    class Meta:
        model = Teacher
        fields = ('user', 'description', 'alerts', 'media', 'id', 'areas_of_specialty', 'group_count', 'private_count', 'first_name', 'last_name', 'phone', 'email')

    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     user = get_user_model().objects.create_user(user_data['email'], **user_data)
    #     return user


class CompanyProfileSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    group_count = serializers.SerializerMethodField()
    private_count = serializers.SerializerMethodField()

    def get_group_count(self, instance):
        return Class.objects.filter(teacher__user=instance.user, is_private=False).count()

    def get_private_count(self, instance):
        return Class.objects.filter(teacher__user=instance.user, is_private=True).count()

    class Meta:
        model = CompanyProfile
        fields = '__all__'


class CompanyProfileWithClassesSerializer(CompanyProfileSerializer):
    classes = serializers.SerializerMethodField()

    def get_classes(self, instance):
        classes = Class.objects.filter(Q(teacher__user=instance.user) | Q(teacher__user__belongs_to=instance.pk))

        today = datetime.now().strftime("%Y-%m-%d")
        classes = classes.filter(
            (Q(until_date__isnull=True) |
             Q(until_date__gte=today)) &
            Q(is_deactivated=False)
        )
        return ClassFullSerializer(classes, many=True).data


class VenueSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Venue
        fields = (
            'user', 'name', 'address', 'description', 'requirements',
            'max_people', 'parking', 'other_services', 'requires_approval',
            'hourly_rate', 'daily_rate', 'minimum_hours'
        )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = get_user_model().objects.create_user(user_data['email'], **user_data)
        instance = Venue.objects.create(
            user=user,
            **validated_data
        )
        return instance


class ClassWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        exclude = ['class_data']


class ClassSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Class
        # fields = '__all__'
        exclude = ['class_data']
        # extra_kwargs = {
        #     'teacher': {'read_only': True},
        # }

    # def create(self, validated_data):
    #     print(validated_data['teacher'], flush=True)
    #     user = self.context['user']
    #     teacher = Teacher.objects.get(
    #         user=user,
    #     )
    #     instance = Class.objects.create(
    #         teacher=teacher.pk,
    #         **validated_data
    #     )

    #     return instance


class ClassFullSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    master_media = serializers.SerializerMethodField()
    class_media = serializers.SerializerMethodField()
    standard_packages = serializers.SerializerMethodField()
    enrolled = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()
    timezone = serializers.SerializerMethodField()

    def get_timezone(self, instance):
        return instance.get_timezone()

    def get_master_media(self, instance):
        cm = ClassMedia.objects.filter(klass=instance).order_by('id')
        if cm:
            return cm[0].class_media.url
        return None

    def get_orders(self, instance):
        orders = ClassLearner.objects.filter(klass=instance).values('data', 'id')
        return ClassLearnerDataSerializer(orders, many=True).data

    def get_enrolled(self, instance):
        EnrModel = GroupEnroll
        if instance.is_private:
            EnrModel = PrivateEnroll
        return EnrModel.objects.filter(
            order__klass=instance,
            #status='approved',
        ).values(
            'date', 'time_from', 'time_to', 'status', 'id', 'order_id',
        )

    def get_class_media(self, instance):
        cm = ClassMedia.objects.filter(klass=instance).order_by('id')
        return ClassMediaSerializer(cm, many=True).data

    def get_standard_packages(self, instance):
        gp_qs = GlobalPackage.objects.filter(teacher=instance.teacher)
        gp = GlobalPackageSerializer(gp_qs, many=True)
        l = []
        if instance.standard_packages:
            l = [x for x in instance.standard_packages if not x.get('isGlobalPackage')]
        l += [x['packages'] for x in gp.data]
        return l

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ClassFullSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    class Meta:
        model = Class
        # fields = '__all__'
        exclude = ['class_data']
        extra_fields = ['master_media', 'class_media']


class ClassMediaSerializer(serializers.ModelSerializer):
    class_media = Base64ImageField()

    class Meta:
        model = ClassMedia
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class TeacherFullSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    classes = serializers.SerializerMethodField()

    def get_classes(self, instance):
        if Class.objects.filter(teacher=instance):
            classes = instance.class_set.all()

            today = datetime.now().strftime("%Y-%m-%d")
            classes = classes.filter(
                (Q(until_date__isnull=True) |
                 Q(until_date__gte=today)) &
                Q(is_deactivated=False)
            )
            # classes = classes.filter(start_date__lte=today)
            # print([v.pk for v in classes], flush=True)
            return ClassSerializer(classes, many=True).data
        return []

    class Meta:
        model = Teacher
        fields = ('user', 'description', 'media', 'id', 'classes', 'areas_of_specialty', 'first_name', 'last_name', 'phone', 'email')


class ShortOrderSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()

    def get_student(self, instance):
        return UserShortSerializer(instance.user).data

    def get_class_name(self, instance):
        return instance.data.get('name')

    class Meta:
        model = ClassLearner
        exclude = ('data', 'session_id')


class ClassLearnerSerializer(serializers.ModelSerializer):
    timezone = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    zoomLink = serializers.SerializerMethodField()

    def get_student(self, instance):
        return UserShortSerializer(instance.user).data

    def get_timezone(self, instance):
        return instance.klass.get_timezone()

    def get_zoomLink(self, instance):
        return instance.klass.zoom_link
    class Meta:
        model = ClassLearner
        fields = '__all__'


class ClassLearnerNoDataSerializer(ClassLearnerSerializer):
    class Meta:
        model = ClassLearner
        exclude = ('data', )


class ClassLearnerNoDataClassSerializer(ClassLearnerSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, instance):
        instance.data.pop('class')
        return instance.data

    class Meta:
        model = ClassLearner
        fields = '__all__'


class OrderShortSerializer(serializers.ModelSerializer):
    package = serializers.SerializerMethodField()
    persons = serializers.SerializerMethodField()

    def get_package(self, instance):
        return instance.data.get('package')

    def get_persons(self, instance):
        return instance.data.get('persons')

    class Meta:
        model = ClassLearner
        fields = ('id', 'amount', 'status', 'learnerNeeds', 'num_lessons', 'reserved_lessons', 'package', 'persons',)


class ClassLearnerDataSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, instance):
        if instance['data'].get('class'):
            del instance['data']['class']
        return instance['data']

    class Meta:
        model = ClassLearner
        fields = ('data', 'id', )


class AddressVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = (
            'address_google', 'address', 'address_city', 'address_zip', 'address_street',
            'address_state', 'teaching_venue', 'lat', 'lng', 'address_country',
        )


class GlobalPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalPackage
        fields = '__all__'


class PrivateEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateEnroll
        fields = '__all__'


class GroupEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupEnroll
        fields = '__all__'


class PrivateEnrollDetailsSerializer(serializers.ModelSerializer):

    student = serializers.SerializerMethodField()
    class_id = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()

    def get_order(self, instance):
        return OrderShortSerializer(instance.order).data

    def get_class_id(self, instance):
        return instance.order.klass.pk

    def get_student(self, instance):
        if instance.order.user:
            return UserSerializer(instance.order.user).data
        else:
            return {
                'email': instance.order.email,
                'phone': instance.order.phone,
                'first_name': instance.order.first_name,
            }

    class Meta:
        model = PrivateEnroll
        fields = '__all__'


class GroupEnrollDetailsSerializer(PrivateEnrollDetailsSerializer):
    order = serializers.SerializerMethodField()

    def get_order(self, instance):
        return OrderShortSerializer(instance.order).data

    class Meta:
        model = GroupEnroll
        fields = '__all__'


class ClassShortSerializer(serializers.ModelSerializer):
    master_media = serializers.SerializerMethodField()
    num_enrolled = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    teacher = TeacherSerializer()
    is_email_boosted = serializers.SerializerMethodField()
    enrolled = serializers.SerializerMethodField()
    timezone = serializers.SerializerMethodField()

    def get_timezone(self, instance):
        return instance.get_timezone()

    def get_master_media(self, instance):
        cm = ClassMedia.objects.filter(klass=instance)
        if cm:
            return cm[0].class_media.url
        return None

    def get_total_amount(self, instance):
        cl = ClassLearner.objects.filter(
            klass=instance,
            is_subscription=False,
        ).exclude(
            status='refund',
        ).aggregate(total_amount=Sum('amount'))
        total = cl['total_amount'] or 0
        # add subscriptions
        cl = ClassLearner.objects.filter(
            klass=instance,
            is_subscription=True,
        ).exclude(
            status='refund',
        ).aggregate(total_paid=Sum('total_paid'), total_ready=Sum('ready_pay'))
        total += cl['total_paid'] or 0
        total += cl['total_ready'] or 0
        return total

    def get_enrolled(self, instance):
        EnrModel = GroupEnroll
        if instance.is_private:
            EnrModel = PrivateEnroll
        return EnrModel.objects.filter(
            order__klass=instance,
            #status='approved',
        ).values(
            'date', 'time_from', 'time_to', 'status', 'id', 'order_id',
        )

    def get_num_enrolled(self, instance):
        return instance.get_num_enrolled()

    def get_is_email_boosted(self, instance):
        em_boost = EmailBoost.objects.filter(klass=instance)
        return em_boost.count() > 0

    class Meta:
        model = Class
        fields = [
            'pk', 'name', 'num_enrolled', 'is_private', 'day_select_type', 'enrolled', 'schedule_dates', 'schedule_excluded', 'start_date', 'until_date',
            'private_className', 'master_media', 'total_amount', 'teacher', 'is_deactivated', 'is_boosted', 'weekdays_schedule',
            'is_email_boosted', 'timezone', 'address', 'address_street', 'address_city', 'address_state', 'address_zip',
            'class_type', 'groupClassSummary', 'zoom_link',
        ]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class DraftClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftClass
        fields = '__all__'


class BoostMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoostMembership
        fields = '__all__'
        write_only_fields = ('stripe_id',)


class EmailBoostSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailBoost
        fields = '__all__'
        write_only_fields = ('stripe_id',)


class MetaTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaTag
        fields = '__all__'


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = '__all__'


class MembershipSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    def get_owner(self, instance):
        return MembershipUserSerializer(instance.owner_user).data

    class Meta:
        model = Membership
        fields = '__all__'


class MembershipStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipStudent
        fields = '__all__'


class MembershipUserSerializer(UserSerializer):
    teacher = serializers.SerializerMethodField()

    def get_teacher(self, instance):
        try:
            return TeacherShortSerializer(Teacher.objects.get(user=instance)).data
        except:
            pass
        return None

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'is_company', 'company_profile', 'teacher')


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)
        # user_data = { # TEST DATA
        #     "id": 12334325,
        #     "email": "test123@gmail.com",
        #     "name": "hamza khan"
        # }
        user_data['email'] = "xyz@gmail.com"
        print(user_data)
        if isinstance(user_data, dict):
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'

            return register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name
            )
        else:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:

            raise serializers.ValidationError('oops, who are you?')
        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name
        )
