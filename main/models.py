# from django.db import models
import PIL, os
from PIL import Image
import stripe
import pytz
import uuid
from datetime import datetime


from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields.jsonb import JSONField
from .utils import save_thumbnail


class User(AbstractUser):
    phone = models.CharField(max_length=255, null=True, blank=True)
    is_company = models.BooleanField(default=False)
    stripe_account_id = models.TextField(null=True, blank=True)
    has_external_account = models.BooleanField(default=False)
    alerts = models.BooleanField(default=False)
    # timezone
    timezone = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    tz_address = models.TextField(null=True, blank=True)
    first_earn_date = models.DateTimeField(null=True, blank=True)
    # capture where registration happens:
    class_id = models.IntegerField(null=True, blank=True)
    is_free_member = models.BooleanField(default=False)
    # student managed by user (teacher or company)
    managed_by = ArrayField(models.IntegerField(), null=True, blank=True)
    # teacher belongs to company, field is company id
    belongs_to = models.IntegerField(null=True, blank=True)
    # text field requested for bulk upload
    source = models.TextField(null=True, blank=True)
    # text field requested for bulk upload
    notes = models.TextField(null=True, blank=True)
    # text field requested for bulk upload
    notes2 = models.TextField(null=True, blank=True)
    auth_provider = models.CharField(max_length=100, default='email')
    media = models.FileField(upload_to='uploads/', null=True, blank=True)

    def save_thumbnail(self):
        if self.media:
            save_thumbnail(self.media)
    
    def __str__(self):
        name = ''
        if self.first_name:
            name += self.first_name + ' '
        if self.last_name:
            name += self.last_name
        if name:
            return name
        return self.email


@receiver(post_save, sender=User)
def sync_user_company_profile(sender, instance, **kwargs):
    if instance.is_company:
        try:
            comp = instance.company
        except ObjectDoesNotExist:
            #print("creating missisng company", flush=True)
            CompanyProfile.objects.create(
                user=instance,
                slug=uuid.uuid4(),
            )


class UserCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_id = models.TextField()
    card_id = models.CharField(max_length=255)
    last4 = models.CharField(max_length=4)
    exp_month = models.CharField(max_length=2)
    exp_year = models.CharField(max_length=4)
    brand = models.CharField(max_length=100)
    is_default = models.BooleanField(default=True)


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "subcategories"

    def __str__(self):
        return '%s => %s' % (self.category, self.name)


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher')
    description = models.TextField(null=True, blank=True)
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    areas_of_specialty = ArrayField(models.TextField(), size=10, null=True, blank=True)
    media = models.FileField(upload_to='uploads/', null=True, blank=True)
    alerts = models.BooleanField(default=False)
    stripe_account_id = models.TextField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=255)
    email = models.EmailField(null=True, blank=True)
    reminder_day = models.BooleanField(default=True)
    reminder_10min = models.BooleanField(default=True)
    reminder_renew = models.BooleanField(default=True)

    def save_thumbnail(self):
        if self.media:
            save_thumbnail(self.media)

    def __str__(self):
        if self.user.is_company:
            return "%s => %s %s" % (self.user.username, self.first_name, self.last_name)
        return self.user.username


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    description = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    media = models.FileField(upload_to='uploads/', null=True, blank=True)
    main_media = models.FileField(upload_to='uploads/', null=True, blank=True)
    replace_logo = models.BooleanField(null=True, default=False)
    slug = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    reminder_day = models.BooleanField(default=True)
    reminder_10min = models.BooleanField(default=True)
    reminder_renew = models.BooleanField(default=True)
    home_url = models.TextField(null=True, blank=True)
    member_center_url = models.TextField(null=True, blank=True)
    member_access_code = models.TextField(null=True, blank=True)
    about_us_url = models.TextField(null=True, blank=True)
    
    def save_thumbnail(self):
        if self.media:
            save_thumbnail(self.media)

    def save_main_thumbnail(self):
        if self.main_media:
            save_thumbnail(self.main_media)

    def __str__(self):
        return self.user.username


class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learner')
    about_me = models.TextField()
    who_takes = models.TextField()

    def __str__(self):
        return self.user.username


class Venue(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='venue')
    name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    requirements = models.TextField()
    max_people = models.IntegerField(null=True, blank=True)
    # Calendar
    # Pricing
    # Upload images, video
    parking = models.CharField(max_length=100)
    other_services = models.TextField(blank=True, null=True)
    requires_approval = models.BooleanField(default=False)
    # step 2
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    # Allows venue to select availability on calendar by hour, day, week, month year out
    minimum_hours = models.IntegerField(null=True, blank=True)


class GlobalPackage(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    packages = JSONField(null=True, blank=True)


class ClassManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class Class(models.Model):

    EXPERIENCE_CHOICES = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Any', 'Any'),
    )
    CLASS_TYPE_CHOICES = (
        ('online', 'online'),
        ('address', 'address'),
        ('venue', 'venue'),
        ('student_location', 'student_location'),
        ('custom', 'custom'),
        ('other', 'other'),
    )
    SHOW_PHONE_RULE_CHOICES = (
        ('text', 'text'),
        ('call', 'call'),
    )
    # used
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.CharField(max_length=140, null=True, blank=True)
    user_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    user_subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    subcategories = ArrayField(models.IntegerField(), size=3, null=True, blank=True)
    experience = ArrayField(models.CharField(max_length=100, choices=EXPERIENCE_CHOICES), size=10, null=True, blank=True)
    group_description = models.TextField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    students_bring = models.TextField(null=True, blank=True)
    teacher_supplies = models.TextField(null=True, blank=True)
    what_else = models.TextField(null=True, blank=True)
    address_google = models.TextField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    address_city = models.TextField(blank=True, null=True)
    address_zip = models.TextField(blank=True, null=True)
    address_street = models.TextField(blank=True, null=True)
    address_state = models.TextField(blank=True, null=True)
    address_country = models.TextField(blank=True, null=True)
    teaching_venue = models.TextField(blank=True, null=True)
    class_type = models.CharField(max_length=100, choices=CLASS_TYPE_CHOICES, default='online')
    rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    group_lesson_length = models.IntegerField(null=True, blank=True)
    group_number_of_lessons = models.IntegerField(null=True, blank=True)
    private_number_of_lessons = ArrayField(models.IntegerField(null=True), size=10, null=True, blank=True)
    instant_booking = models.BooleanField(null=True, blank=True)
    private_lesson_length = ArrayField(models.IntegerField(null=True), size=10, null=True, blank=True)
    schedule_dates = JSONField(default=list, null=True, blank=True)
    schedule_from = models.CharField(max_length=30, null=True, blank=True)
    schedule_to = models.CharField(max_length=30, null=True, blank=True)
    schedule_excluded = ArrayField(models.CharField(max_length=30), null=True, blank=True)
    weekdays_schedule = JSONField(default=list, null=True, blank=True)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    is_master = models.BooleanField(default=False)
    day_select_type = models.TextField(null=True, blank=True)
    flexible_dates = models.BooleanField(default=False)
    until_date = models.TextField(null=True, blank=True)
    standard_packages = JSONField(default=list, null=True, blank=True)
    custom_packages = JSONField(default=list, null=True, blank=True)
    group_package_type = models.CharField(max_length=30, null=True, blank=True)
    teaching_country = models.TextField(null=True, blank=True)
    private_class_website = models.TextField(null=True, blank=True)
    private_className = models.TextField(null=True, blank=True)
    location_other = models.TextField(null=True, blank=True)
    currency = models.TextField(null=True, blank=True)
    start_date = models.TextField(null=True, blank=True)
    drop_in_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    timezone = models.TextField(null=True, blank=True)
    groupClassSummary = models.TextField(null=True, blank=True)
    maxSize = models.IntegerField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    point = models.PointField(geography=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    class_data = JSONField(default=dict, null=True, blank=True)
    is_deactivated = models.BooleanField(default=False, blank=True)
    can_book = models.BooleanField(default=True, blank=True)
    can_book_url = models.TextField(null=True, blank=True)
    can_pay = models.BooleanField(default=True, blank=True)
    is_price_hidden = models.BooleanField(default=False, blank=True)
    is_boosted = models.BooleanField(default=False, blank=True)
    boost_weekday = models.IntegerField(null=True, blank=True)
    boost_option_id = models.IntegerField(null=True, blank=True)
    is_paid_by_teacher = models.BooleanField(null=True, default=True)
    activated_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    show_email = models.BooleanField(default=False, blank=True, null=True)
    show_phone = models.BooleanField(default=False, blank=True, null=True)
    show_phone_rule = models.CharField(max_length=32, choices=SHOW_PHONE_RULE_CHOICES, default='text')
    is_premium_community = models.BooleanField(default=False)
    zoom_link = models.TextField(null=True, blank=True)

    all_objects = models.Manager()
    objects = ClassManager()

    def get_num_enrolled(self):
        if self.is_private:
            return PrivateEnroll.objects.filter(order__klass=self).exclude(status='rejected').count()
        else:
            return GroupEnroll.objects.filter(order__klass=self).exclude(status='rejected').count()

    def get_timezone(instance):
        if not instance.timezone:
            return 'US/Central'
        return instance.timezone

    def __str__(self):
        return self.name or '__no name__'

    class Meta:
        verbose_name_plural = "classes"


class ClassMedia(models.Model):
    klass = models.ForeignKey(Class, on_delete=models.CASCADE)
    class_media = models.FileField(upload_to='uploads/', null=True, blank=True)

    def save_thumbnail(self, size=300):
        save_thumbnail(self.class_media)


class Payment(models.Model):
    payment_id = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.TextField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "%s => $%s (%s)" % (self.user, self.amount, self.created_at)


class PaymentByTeacher(models.Model):
    charge_id = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.TextField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    single_class = models.IntegerField(null=True, blank=True)
    classes = ArrayField(models.IntegerField(), null=True, blank=True)
    is_draft = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user} => {self.amount} cents [{self.status}]"

# Orders
class ClassLearner(models.Model):
    alerts = models.BooleanField(default=False)
    klass = models.ForeignKey(Class, on_delete=models.CASCADE)
    learnerNeeds = models.TextField(null=True)
    session_id = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    data = JSONField(default=dict, null=True, blank=True)
    status = models.CharField(max_length=100, default='wait_payment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reserved_lessons = models.IntegerField(null=False, default=0)
    num_lessons = models.IntegerField(null=False, default=1)
    num_lessons_per_interval = models.IntegerField(null=True)
    #  paid to teacher
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    #  with all fees
    amount_full = models.DecimalField(max_digits=6, decimal_places=2)
    no_pay = models.BooleanField(default=False)
    # 1 - ready to pay, 2 - paid to teacher, 3 - stripe paid is false, required investiagtion
    paid_status = models.IntegerField(null=True, blank=True)
    payment = models.ForeignKey(Payment, null=True, on_delete=models.CASCADE, related_name='payments')
    # subscription
    is_subscription = models.BooleanField(default=False)
    interval = models.CharField(max_length=20, null=True)
    interval_count = models.IntegerField(null=True)
    end_at = models.DateTimeField(null=True)

    current_period_start = models.IntegerField(null=True)
    current_period_end = models.IntegerField(null=True)
    # paid to teacher
    ready_pay = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    total_paid = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    payments = ArrayField(models.IntegerField(), null=True, blank=True)

    def update_reserved_lessons(self):
        if self.klass.is_private:
            self.reserved_lessons = self.privateenroll_set.exclude(status='rejected').count()
        else:
            self.reserved_lessons = self.groupenroll_set.exclude(status='rejected').count()
        # funds are ready for release
        if self.reserved_lessons and not self.no_pay and not self.paid_status:
            self.paid_status = 1
        self.save()

    def update_subsciption_data(self):
        stripe.api_key = os.environ['STRIPE_SECRET_KEY']
        s = stripe.Subscription.retrieve(self.session_id)
        self.status = s['status']

        interval = s['current_period_end'] - s['current_period_start']
        num_ints = (s['current_period_end'] - s['start_date']) / interval
        num_ints = int(num_ints)
        assert num_ints >= 1
        if self.status in ('active', 'canceled'):
            self.num_lessons = num_ints * self.num_lessons_per_interval
        if s['cancel_at'] is not None:
            assert s['cancel_at'] + interval > s['current_period_end']
        if not self.ready_pay:
            self.ready_pay = 0
        if not self.total_paid:
            self.total_paid = 0
        if self.ready_pay + self.total_paid < num_ints*self.amount:
            self.ready_pay = num_ints*self.amount - self.total_paid
        self.current_period_start = s['current_period_start']
        self.current_period_end = s['current_period_end']
        self.save()

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return '[%s] %s => %s' % (self.pk, self.user, self.klass)


class PrivateEnroll(models.Model):
    order = models.ForeignKey(ClassLearner, on_delete=models.CASCADE)
    date = models.TextField(null=False, blank=False)
    time_from = models.TextField(null=False, blank=False)
    time_to = models.TextField(null=False, blank=False)
    status = models.TextField(null=False, default='requested')
    time_from_gmt = models.DateTimeField(null=True)
    notification_sent = models.BooleanField(default=False)
    decline_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    secret = models.TextField(null=True, blank=True)

    def __str__(self):
        return "[%s] %s %s" % (self.order.pk, self.date, self.time_from)


class GroupEnroll(models.Model):
    order = models.ForeignKey(ClassLearner, on_delete=models.CASCADE)
    date = models.TextField(null=False, blank=False)
    time_from = models.TextField(null=False, blank=False)
    time_to = models.TextField(null=False, blank=False)
    status = models.TextField(null=False, default='approved')
    time_from_gmt = models.DateTimeField(null=True)
    notification_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    klass = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    text = models.TextField()
    parent_id = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name='replies')
    thread_id = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name='thread_messages')


class DraftClass(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class_data = JSONField(default=dict, null=True, blank=True)


class TeacherProfileLog(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    data = JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    headers = JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return "%s at %s" % (self.teacher, self.created_at)


class Newsletter(models.Model):
    email = models.EmailField()
    city = models.TextField()
    is_learner = models.BooleanField()
    is_teacher = models.BooleanField()
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return self.email


class BoostMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boosted')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    num_classes = models.IntegerField()
    is_monthly = models.BooleanField(default=False)
    name = models.TextField(null=True, blank=True)
    valid = models.BooleanField(default=True)
    status = models.TextField(default=None)
    stripe_id = models.TextField(null=True)
    option_id = models.IntegerField()


class EmailBoost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_boosted')
    klass = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='email_boosted_classes')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    num_classes = models.IntegerField()
    is_monthly = models.BooleanField(default=False)
    valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    status = models.TextField(default=None)
    stripe_id = models.TextField()
    option_id = models.IntegerField()

    def __str__(self):
        return f"{self.user} - {self.klass} => ${self.amount}"


class Event(models.Model):
    name = models.TextField()
    multiple_dates = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    companies = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='uploads/events/')
    order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if not self.name:
            return '__NO NAME__'
        return self.name


class MetaTag(models.Model):
    route = models.CharField(max_length=255, unique=True)
    title = models.TextField()
    metatag = models.TextField()

    def __str__(self):
        return self.route


class TeacherMessage(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    teacher_to = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='messages')
    allow_contact = models.BooleanField()

    def __str__(self):
        return "%s => %s: %s" % (self.user_from, self.teacher_to, self.message)


class ChargeLog(models.Model):
    charge_id = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='charges')
    amount = models.IntegerField()
    status = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)


class AddStudent(models.Model):
    email = models.EmailField()
    name = models.TextField()
    phone = models.TextField()
    class_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} => class_id: {self.class_id}"


class CardError(models.Model):
    json = models.TextField()
    req = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='card_errors')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.req


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    settings = JSONField(null=True, blank=True)


class DeletedStudent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deleted_students')
    student_id = models.IntegerField()
    deleted_at = models.DateTimeField(auto_now_add=True)


class ExternalCalendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='external_calendars')
    provider_type = models.TextField()
    provider_id = models.TextField()
    data = JSONField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'provider_type', 'provider_id'], name='user_provider'),
        ]


class Membership(models.Model):
    owner_user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(null=True, blank=True)
    currency = models.TextField(null=True, blank=True)
    weekly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    monthly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    yearly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    media = models.FileField(upload_to='uploads/', null=True, blank=True)
    isDirectoryEnabled = models.BooleanField(null=True, default=False)
    isDMEnabled = models.BooleanField(null=True, default=False)
    isChatEnabled = models.BooleanField(null=True, default=False)
    isUploadAllowed = models.BooleanField(null=True, default=False)
    isUploadRequired = models.BooleanField(null=True, default=False)
    isAboutAllowed = models.BooleanField(null=True, default=False)
    isAboutRequired = models.BooleanField(null=True, default=False)
    isTitleAllowed = models.BooleanField(null=True, default=False)
    isTitleRequired = models.BooleanField(null=True, default=False)
    isCityAllowed = models.BooleanField(null=True, default=False)
    isCityRequired = models.BooleanField(null=True, default=False)
    isProjectsAllowed = models.BooleanField(null=True, default=False)
    isProjectsRequired = models.BooleanField(null=True, default=False)
    isSocialAllowed = models.BooleanField(null=True, default=False)
    isSocialRequired = models.BooleanField(null=True, default=False)
    isPhoneAllowed = models.BooleanField(null=True, default=False)
    isPhoneRequired = models.BooleanField(null=True, default=False)
    isEmailAllowed = models.BooleanField(null=True, default=False)
    isEmailRequired = models.BooleanField(null=True, default=False)
    isDocumentAllowed = models.BooleanField(null=True, default=False)
    isDocumentRequired = models.BooleanField(null=True, default=False)
    customInterestsField = models.TextField(null=True, blank=True)
    customSkillsField = models.TextField(null=True, blank=True)
    customLevelsField = models.TextField(null=True, blank=True)

    def save_thumbnail(self):
        if self.media:
            save_thumbnail(self.media)


class MembershipStudent(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name='students')
    currency = models.TextField(null=True, blank=True)
    weekly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    monthly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    yearly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    period = models.TextField(null=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    session_id = models.TextField(null=True)
    status = models.CharField(max_length=100, default='wait_payment')
    updated_at = models.DateTimeField(auto_now=True)
    #  paid to teacher
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    #  with all fees
    amount_full = models.DecimalField(max_digits=6, decimal_places=2)
    end_at = models.DateTimeField(null=True)
    current_period_start = models.IntegerField(null=True)
    current_period_end = models.IntegerField(null=True)
    total_paid = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    payments = ArrayField(models.IntegerField(), null=True, blank=True)
    is_active = models.BooleanField(default=True)
    invoices = JSONField(default=list)
    is_permanent = models.BooleanField(default=False)
    title = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    document = models.TextField(null=True, blank=True)
    social = models.TextField(null=True, blank=True)
    website = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    level = models.TextField(null=True, blank=True)
    skill = models.TextField(null=True, blank=True)
    interest = models.TextField(null=True, blank=True)

    def update_subsciption_data(self):
        if self.is_permanent:
            self.deactivated_at = None
            self.is_active = True
            self.save()
            return
        stripe.api_key = os.environ['STRIPE_SECRET_KEY']
        s = stripe.Subscription.retrieve(self.session_id)
        self.status = s['status']
        if self.status == 'canceled' or self.status == 'unpaid':
            # process cancelation
            self.deactivated_at = datetime.now()
            self.is_active = False
            self.save()
            return
        interval = s['current_period_end'] - s['current_period_start']
        num_ints = (s['current_period_end'] - s['start_date']) / interval
        num_ints = int(num_ints)
        assert num_ints >= 1
        if s['cancel_at'] is not None:
            assert s['cancel_at'] + interval > s['current_period_end']
        self.total_paid = float(num_ints*s['plan']['amount']/100)
        self.current_period_start = s['current_period_start']
        self.current_period_end = s['current_period_end']
        invoices = stripe.Invoice.list(subscription=self.session_id)
        self.invoices = [{
            'id': inv['id'],
            'created': inv['created'],
            'currency': inv['currency'],
            'amount_paid': inv['amount_paid'] / 100,
            'total': inv['total'] / 100,
        } for inv in filter(lambda x: x['paid'], invoices)]
        print(self.invoices)
        self.save()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'membership', 'created_at'], name='user_membership'),
        ]


# class Community(models.Model):
#     pass


class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='uploads/discussions/', null=True, blank=True)
    type= models.CharField(max_length=100, choices=(
        ("C", "COMMUNITY"),
        ("E", "EVENT"),
        ("T", "TOPIC"),
    ), default="C")
    users = models.ManyToManyField(User, blank=True, related_name="members")
    blocked_users = models.ManyToManyField(User, blank=True, related_name='block_users')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/chat/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_reply = models.BooleanField(default=False)
    is_liked = models.BooleanField(default=False)
    top_comment = models.BooleanField(default=False) # FOR THE TOP COMMENT HANDLED AS DESCRIPTION

    def __str__(self):
        return f"{self.content[0:7]}... By {self.user}"
