from django.db import migrations
from django.conf import settings
import PIL, os
from PIL import Image
from main.utils import save_thumbnail


def update_media(apps, schema_editor):
    Teacher = apps.get_model('main', 'Teacher')
    CompanyProfile = apps.get_model('main', 'CompanyProfile')
    maxsize = (300, 300)
    for c in Teacher.objects.all():
        if c.media:
            print(c.media)
            save_thumbnail(c.media)
    for c in CompanyProfile.objects.all():
        if c.media:
            print(c.media)
            save_thumbnail(c.media)

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0113_auto_20200318_1203'),
    ]

    operations = [
        migrations.RunPython(update_media),
    ]
