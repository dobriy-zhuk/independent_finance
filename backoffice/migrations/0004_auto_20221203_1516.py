# Generated by Django 3.2.7 on 2022-12-03 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0003_alter_meeting_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='address',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='link',
            field=models.CharField(default='f480806e20', max_length=300),
        ),
    ]
