import csv
import os
import stripe
import operator

from django.contrib import admin, messages
from django.utils.translation import ngettext
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponse

from .models import (
    Category, SubCategory, User, Teacher, Class, ClassLearner,
    GlobalPackage, DraftClass, CompanyProfile, PrivateEnroll,
    TeacherProfileLog, UserCard, GroupEnroll, Newsletter,
    BoostMembership, Event, Payment, MetaTag, TeacherMessage,
    PaymentByTeacher, EmailBoost, CardError, Discussion, Comment
)
from .forms import MetatagForm
from teachbeach.forms import AdminUserChangeForm

def get_stats(user_type, u, company_name, classes):
    num_classes = 0
    revenue = 0
    categories = {}
    # total_students = 0
    for c in classes:
        if c.subcategories:
            for cat_id in c.subcategories:
                if cat_id not in categories:
                    categories[cat_id] = 0
                categories[cat_id] += 1
        class_revenue = 0
        students = 0
        orders = ClassLearner.objects.filter(klass=c)
        for o in orders:
            if not o.no_pay:
                class_revenue += o.amount
            students += 1

        num_classes += 1
        # total_students += students
        revenue += class_revenue
    if categories:
        max_cat_id = max(categories.items(), key=operator.itemgetter(1))[0]
        try:
            max_cat = SubCategory.objects.get(pk=max_cat_id).name
        except:
            max_cat = None  # deleted already...
    else:
        max_cat = None
    return [user_type, u.first_name, u.last_name, company_name, u.phone, u.email, revenue, num_classes, max_cat]

def export_csu(modeladmin, request, queryset):
    users = User.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csu.csv"'

    writer = csv.writer(response)
    writer.writerow(['User type', 'First', 'Last', 'Company Name', 'Phone', 'Email', 'Revenues', '#classes', 'Main category'])

    for u in users:
        user_type = 'Company user' if u.is_company else 'Teacher user'
        company_name = None
        if u.email:
            if u.is_company:
                try:
                    company_name = u.company.name
                except:
                    pass
            classes = Class.objects.filter(teacher__user=u)
            row = get_stats(user_type, u, company_name, classes)
            writer.writerow(row)

    orgs = User.objects.filter(is_company=True)
    for t in Teacher.objects.filter(user__in=orgs):
        user_type = 'Company teacher with phone number'
        classes = Class.objects.filter(teacher=t)
        company_name = None
        if t.user.is_company:
            try:
                company_name = t.user.company.name
            except:
                pass

        row = get_stats(user_type, t, company_name, classes)
        writer.writerow(row)

    return response

export_csu.short_description = "Export CSU (select any user, it's django limitation)"


def export_students(modeladmin, request, queryset):
    users = User.objects.filter(pk__in=ClassLearner.objects.all().values('user'))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email'])
    for u in users:
        if u.email:
            writer.writerow([u.first_name, u.last_name, u.email])
    return response

export_students.short_description = "Export student emails (select any user, it's django limitation)"


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('Login', {
            'fields': [
                'email',
                'first_name',
                'last_name',
                'password',
                'phone',
                'is_company',
                'is_free_member',
                'timezone',
                'timezone_to_classes',
            ]
        }),
    )
    actions = [export_students, export_csu]
    form = AdminUserChangeForm
    # add_form = AdminUserCreationForm

UserAdmin.list_display += ('has_external_account', 'class_id')
UserAdmin.list_filter += ('has_external_account',)


class MetatagAdmin(admin.ModelAdmin):
    form = MetatagForm
    list_display = ('route', 'title', 'metatag',)



class ClassLearnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'klass', 'status', 'amount', 'is_subscription',
        'created_at', )
    list_filter = ('is_subscription', )
    actions = ['refund_order', 'cancel']

    def cancel(self, request, queryset):
        ok = 0
        for c in queryset:
            if not c.no_pay and c.is_subscription and c.status == 'active' and c.session_id:
                ok += 1
                stripe.api_key = os.environ['STRIPE_SECRET_KEY']

                res = stripe.Subscription.delete(c.session_id)
                c.valid = False
                c.status = 'canceled'
                c.save()

        self.message_user(request, ngettext(
                '%d subscription cancelled.',
                '%d subscriptions cancelled.',
                ok,
            ) % ok, messages.SUCCESS)

    cancel.short_description = 'Cancel Subscription'

    def refund_order(self, request, queryset):
        ok = 0
        for c in queryset:
            if not c.no_pay and c.status == 'succeeded' and c.session_id:
                ok += 1
                stripe.api_key = os.environ['STRIPE_SECRET_KEY']

                s = stripe.Charge.retrieve(c.session_id)

                refund = stripe.Refund.create(
                    charge=c.session_id,
                )

                c.status = 'refund'
                c.save()

        self.message_user(request, ngettext(
                '%d refund done.',
                '%d refunds done.',
                ok,
            ) % ok, messages.SUCCESS)

    refund_order.short_description = 'Refund'


class BoostMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'is_monthly', 'valid')
    actions = ['cancel']

    def cancel(self, request, queryset):
        ok = 0
        for c in queryset:
            if c.valid and c.stripe_id:
                ok += 1
                stripe.api_key = os.environ['STRIPE_SECRET_KEY']

                res = stripe.Subscription.delete(c.stripe_id)
                c.valid = False
                c.status = 'canceled'
                c.save()

        self.message_user(request, ngettext(
                '%d subscription cancelled.',
                '%d subscriptions cancelled.',
                ok,
            ) % ok, messages.SUCCESS)

    cancel.short_description = 'Cancel Subscription'


class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'teacher')


admin.site.register([
    Category, SubCategory, Teacher,
    GlobalPackage, DraftClass,
    CompanyProfile, PrivateEnroll, TeacherProfileLog,
    UserCard, GroupEnroll, Newsletter,
    Event, Payment, TeacherMessage, PaymentByTeacher,
    EmailBoost, CardError,
])
admin.site.register(User, UserAdmin)
admin.site.register(MetaTag, MetatagAdmin)
admin.site.register(ClassLearner, ClassLearnerAdmin)
admin.site.register(BoostMembership, BoostMembershipAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Discussion)
admin.site.register(Comment)

