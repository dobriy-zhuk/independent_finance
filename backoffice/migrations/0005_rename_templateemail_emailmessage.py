# Generated by Django 3.2.7 on 2021-12-08 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0004_remove_templateemail_responsible_manager'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TemplateEmail',
            new_name='EmailMessage',
        ),
    ]
