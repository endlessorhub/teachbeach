import re
from datetime import datetime, timedelta

from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from main.models import User, Teacher, Class

class PasswordChangeForm(auth_forms.PasswordChangeForm):
    def clean_new_password1(self):
        new_password = self.cleaned_data['new_password1']

        if len(new_password) < 8:
            raise forms.ValidationError("Password is too short (min 8 characters.)")
        # it's too difficult for users
        # non_alp = re.search(r"[0-9\!@#\$%&\*\(\)]", new_password)
        # if not non_alp:
        #     raise forms.ValidationError("Password must contain at least one non-alphabetic character")

        az = re.search('[a-zA-Z]', new_password)
        if not az:
            raise forms.ValidationError("Password must contain at least one alphabetic character")

        return new_password

    def save(self, commit=True):
        user = super(PasswordChangeForm, self).save(commit)
        user.force_change_password = False
        user.save()
        return user


class FinishPasswordResetForm(auth_forms.SetPasswordForm):
    uidb64 = forms.CharField(max_length=20)
    token = forms.CharField(max_length=50)

    def clean(self):
        uidb64 = self.cleaned_data['uidb64']
        try:
            # urlsafe_base64_decode() decodes to bytestring on Python 3
            uid = force_text(urlsafe_base64_decode(uidb64))
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise forms.ValidationError("Invalid token")

        token = self.cleaned_data['token']
        if not default_token_generator.check_token(self.user, token):
            raise forms.ValidationError("Invalid token")

        return self.cleaned_data


class AdminUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"../password/\">this form</a>."
    )

    timezone_to_classes = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = User
        fields = "__all__"

    def clean_password(self):
        return self.initial["password"]

    def save(self, commit=True):
        user = super(AdminUserChangeForm, self).save(commit)
        if self.cleaned_data.get('timezone_to_classes', None):
            teachers = Teacher.objects.filter(user=user)
            Class.objects.filter(teacher__in=teachers).update(timezone=user.timezone)
        return user
