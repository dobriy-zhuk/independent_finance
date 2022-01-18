# Generated by Django 3.2.7 on 2021-12-10 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(editable=False, max_length=200, unique=True)),
                ('image', models.FileField(default='blog/logo-rus.png', upload_to='blog/')),
                ('meta_title', models.CharField(max_length=80)),
                ('meta_description', models.CharField(max_length=160)),
                ('meta_keywords', models.CharField(default='', max_length=1000)),
                ('text', models.TextField()),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]
