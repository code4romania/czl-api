from __future__ import unicode_literals

import os.path
import yaml
from django.conf import settings
from django.db import migrations


SOURCE_FILE = os.path.join(settings.BASE_DIR, 'data', 'institutions.yaml')

def forwards_func(apps, schema_editor):
    Institution = apps.get_model("core", "Institution")
    db_alias = schema_editor.connection.alias

    with open(SOURCE_FILE, 'r') as f:
        institutions = yaml.load(f)

        Institution.objects.using(db_alias).bulk_create([
            Institution(**inst) for inst in institutions
        ])

def reverse_func(apps, schema_editor):
    Institution = apps.get_model("core", "Institution")
    db_alias = schema_editor.connection.alias

    with open(SOURCE_FILE, 'r') as f:
        institutions = yaml.load(f)

        Institution.objects.using(db_alias).filter(
            id__in=[inst['id'] for inst in institutions]
        ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
