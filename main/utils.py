import os
import io
from django.conf import settings
from io import StringIO
from html.parser import HTMLParser
from twilio.rest import Client
import PIL, os
from PIL import Image
from datetime import datetime
from django.core.mail.message import (
    EmailMultiAlternatives,
)
from django.core.mail import get_connection
import boto3

def send_mail_reply_to(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=None, reply_to=None):
    """
    Easy wrapper for sending a single message to a recipient list. All members
    of the recipient list will see the other recipients in the 'To' field.

    If from_email is None, use the DEFAULT_FROM_EMAIL setting.
    If auth_user is None, use the EMAIL_HOST_USER setting.
    If auth_password is None, use the EMAIL_HOST_PASSWORD setting.

    Note: The API for this method is frozen. New code wanting to extend the
    functionality should use the EmailMessage class directly.
    """
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    mail = EmailMultiAlternatives(subject, message, from_email, recipient_list, connection=connection, reply_to=reply_to)
    if html_message:
        mail.attach_alternative(html_message, 'text/html')

    return mail.send()

def send_text(body, to, from_=settings.TWILIO_SEND_FROM):
    if 'TWILIO_ACCOUNT_SID' not in os.environ:
        print('text message: %s to %s' % (body, to), flush=True)
        return
    # # so far disabled
    # if to != '+14088929815':
    #     body = 'to %s: %s' % (to, body)
    #     to = '+14088929815'

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            body=body,
            from_=from_,
            to=to,
            # to='+14088929815'
            # to='+79119129916'
        )
    except:
        pass

def save_thumbnail(image_file, size=300):
    maxsize = (size, size)
    image = Image.open(image_file)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    image.thumbnail(maxsize, PIL.Image.ANTIALIAS)
    file, ext = os.path.splitext(image_file.name)
    if ext.startswith('.'):
        ext = ext[1:]
    if not ext:
        ext = 'png'
    if os.environ['FILE_UPLOAD_STORAGE'] == "s3":
        region = os.environ['AWS_REGION']
        key = os.environ['AWS_ACCESS_KEY_ID']
        secret = os.environ['AWS_SECRET_ACCESS_KEY']
        bucket = os.environ['AWS_S3_BUCKET']
        in_mem_file = io.BytesIO()
        format = ext
        if format.lower() == 'jpg':
            format = 'JPEG'
        image.save(in_mem_file, format=format)
        in_mem_file.seek(0)
        s3_client = boto3.client('s3', region_name=region, aws_access_key_id=key, aws_secret_access_key=secret)
        s3_client.upload_fileobj(in_mem_file, bucket, file + ".thumbnail%s.%s" % (size, ext))
    else:
        image_path = os.path.join(settings.MEDIA_ROOT, file + ".thumbnail%s.%s" % (size, ext))
        image.save(image_path)


def format_date_time(d, t):
    dt = '%s %s' % (d, t)
    date_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
    return date_object.strftime('%B %d at %I:%M %p')


def format_date_time_from_to(d, f, to):
    dt = '%s %s' % (d, f)
    tt = '%s %s' % (d, to)
    date_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
    d = date_object.strftime('%B %d at %I:%M %p')
    date_object = datetime.strptime(tt, '%Y-%m-%d %H:%M')
    d += ' to ' + date_object.strftime('%I:%M %p, %Y')
    return d


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_message_sign(request, cp_class):
    return ("Express from "+cp_class.objects.get(user=request.user).name+"\n" if request.user.is_company else '') + "Powered by Teachbeach"

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d+' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'br':
            self.text.write('\n')
        if tag == 'a':
            for k, v in attrs:
                if k == 'href':
                    self.text.write(v+' ')

    def handle_endtag(self, tag):
        if tag == 'div':
            self.text.write(' \n ')

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
