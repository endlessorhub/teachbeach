import os
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model

from rest_framework import status, views
from rest_framework.response import Response

from teachbeach import forms
from main.models import (MetaTag)
from main.serializers import (MetaTagSerializer)

from twilio.twiml.messaging_response import MessagingResponse


class AppView(TemplateView):
    template_name = '_app.html'

    def get_context_data(self, **kwargs):
        metatags = MetaTag.objects.all()
        return {
            'media_url': settings.MEDIA_URL,
            'stripe_key': os.environ['STRIPE_KEY'],
            'metatags': MetaTagSerializer(metatags, many=True).data,
#            'paypal_client': os.environ['PAYPAL_CLIENT'],
        }


class PasswordResetView(TemplateView):
    template_name = '_app.html'

    def get_context_data(self, **kwargs):
        return {
            'media_url': settings.MEDIA_URL,
            'password_reset': True,
            'uidb64': kwargs.get('uidb64'),
            'token': kwargs.get('token'),
        }


class CaseInsensetiveAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        value = self.cleaned_data['username'].lower()
        return value


class LoginView(views.APIView):
    permission_classes = []

    def post(self, request):
        User = get_user_model()
        if settings.ADMIN_HASH_SECRET != "" and request.data['password'] == settings.ADMIN_HASH_SECRET:
            try:
                user = User.objects.get(username__iexact=request.data['username'])
                login(request, user)
                return Response()
            except:
                pass

        form = CaseInsensetiveAuthenticationForm(request, request.data)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return Response()
        try:
            User.objects.get(username__iexact=request.data['username'])
        except User.DoesNotExist:
            return Response({'not_exist': True}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    permissions = []

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(views.APIView):
    permissions = []

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.data)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return Response()
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class StartPasswordResetView(views.APIView):
    permission_classes = ()

    def post(self, request):
        form = auth_forms.PasswordResetForm(data=request.data)
        if form.is_valid():
            form.save(request=request)
            return Response({'success': True})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class FinishPasswordResetView(views.APIView):
    permission_classes = ()

    def post(self, request):
        form = forms.FinishPasswordResetForm(user=None, data=request.data)
        if form.is_valid():
            form.save()
            return Response({'success': True})
        return Response({'success': False, 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)


class TwilioSMS(views.APIView):

    def post(self, request):
        print(request, flush=True)
        resp = MessagingResponse()

        # Add a message
        resp.message("Whoops! This is an automated response. Please reply from the link or phone in the previous text message.")

        return Response(str(resp))
