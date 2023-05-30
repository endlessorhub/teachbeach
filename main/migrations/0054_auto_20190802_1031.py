from django.db import migrations
import pytz
from datetime import datetime


def backward(apps, schema_editor):
    pass

def update_classes(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    Enroll = apps.get_model('main', 'GroupEnroll')
    for enr in Enroll.objects.all():

        class_tz = pytz.timezone(enr.order.klass.timezone)
        x = datetime.strptime('%s %s' % (enr.date, enr.time_from), '%Y-%m-%d %H:%M')
        x = class_tz.localize(x)
        enr.time_from_gmt = x

        enr.save()

    Enroll = apps.get_model('main', 'PrivateEnroll')
    for enr in Enroll.objects.all():

        class_tz = pytz.timezone(enr.order.klass.timezone)
        x = datetime.strptime('%s %s' % (enr.date, enr.time_from), '%Y-%m-%d %H:%M')
        x = class_tz.localize(x)
        enr.time_from_gmt = x

        enr.save()



class Migration(migrations.Migration):

    reversible = True

    dependencies = [
        ('main', '0053_auto_20190802_1012'),
    ]

    operations = [
        migrations.RunPython(update_classes, backward),
        # migrations.RunPython(backward),
    ]
