# Generated by Django 3.2.7 on 2022-12-03 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.IntegerField(blank=True)),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'ApplicantContents',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='My Company', max_length=300)),
                ('description', models.CharField(blank=True, max_length=300)),
                ('taxpayerNumber', models.CharField(max_length=300, unique=True)),
                ('country', models.CharField(blank=True, choices=[('UK', 'UK'), ('USA', 'USA'), ('Canada', 'Canada')], default='USA', help_text='Countries', max_length=20)),
                ('mailing_address', models.TextField(blank=True)),
                ('physical_address', models.TextField(blank=True)),
                ('currency', models.CharField(blank=True, choices=[('USD', 'USD'), ('EURO', 'EURO'), ('POUND', 'POUND')], default='USD', help_text='Currencies', max_length=20)),
                ('date_added', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('comment', models.TextField(blank=True)),
                ('professional_area', models.CharField(blank=True, choices=[('it', 'IT'), ('education', 'Education'), ('hr', 'HR'), ('finance', 'Finance')], default='it', help_text='Professional Areas', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='CompletedCourses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='USA', max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='USD', max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default=uuid.uuid4, max_length=100, unique=True)),
                ('title', models.CharField(default='Seller', max_length=100)),
                ('description', models.CharField(default='', max_length=500)),
                ('skills', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('open', 'open'), ('archive', 'archive'), ('draft', 'draft')], default='draft', max_length=50)),
                ('date_added', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.company')),
            ],
            options={
                'verbose_name_plural': 'jobs',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=100)),
                ('bank_details', models.TextField(blank=True)),
                ('comment', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'managers',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('applied_for', models.CharField(choices=[('HR', 'HR'), ('STAFF', 'STAFF'), ('APPLICANT', 'APPLICANT')], max_length=50)),
                ('status', models.CharField(choices=[('test', 'test'), ('simulator', 'simulator'), ('interview', 'interview')], default='test', max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Quizes',
            },
        ),
        migrations.CreateModel(
            name='StaffSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Indeed', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Standard', max_length=50)),
                ('price', models.IntegerField(default=25)),
                ('candidates', models.IntegerField(default=100)),
                ('additional_candidate_price', models.FloatField(default=1.2)),
                ('tests', models.IntegerField(default=5)),
                ('valid_until', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('ats_integration', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Subscriptions',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('salary', models.IntegerField(blank=True, default=0)),
                ('currency', models.CharField(blank=True, default='EUR', max_length=4)),
                ('phone', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Archive', 'Archive'), ('Interview', 'Interview'), ('Learning', 'Learning'), ('Work', 'Work')], default='Active', max_length=50)),
                ('comment', models.TextField(blank=True)),
                ('cv', models.FileField(default='blog/logo-rus.png', upload_to='documents/')),
                ('cv_uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('completed_courses', models.ManyToManyField(blank=True, to='backoffice.CompletedCourses')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.job')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backoffice.staffsource')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'staff',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('language', models.CharField(blank=True, max_length=200)),
                ('currency', models.CharField(default='RUB', max_length=4)),
                ('phone', models.CharField(blank=True, max_length=100)),
                ('tariff', models.PositiveIntegerField(default=0)),
                ('date_added', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('comment', models.TextField(blank=True)),
                ('responsible_manager', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='backoffice.manager')),
            ],
            options={
                'verbose_name_plural': 'settings',
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Interview', max_length=300)),
                ('meeting_time', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('link', models.CharField(default='1b84595d68', max_length=300)),
                ('applicant', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='backoffice.staff')),
                ('company', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='backoffice.company')),
                ('questions', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='backoffice.quiz')),
                ('responsible_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.manager')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='responsible_manager',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='backoffice.manager'),
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=300)),
                ('template', models.TextField(blank=True, default='')),
                ('comment', models.TextField(blank=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.company')),
            ],
            options={
                'verbose_name_plural': 'EmailTemplates',
            },
        ),
        migrations.CreateModel(
            name='EmailMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(default='', max_length=300)),
                ('body', models.TextField(default='')),
                ('language', models.CharField(blank=True, max_length=200)),
                ('date_added', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('comment', models.TextField(blank=True)),
                ('receivers', models.ManyToManyField(blank=True, to='backoffice.Staff')),
            ],
            options={
                'verbose_name_plural': 'EmailMessages',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Training', max_length=250)),
                ('body', models.TextField(default='')),
                ('files', models.FileField(blank=True, null=True, upload_to='courses_files/')),
                ('date_added', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('comment', models.TextField(blank=True)),
                ('job_title', models.ManyToManyField(blank=True, to='backoffice.Job')),
            ],
            options={
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.AddField(
            model_name='completedcourses',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.course'),
        ),
        migrations.AddField(
            model_name='completedcourses',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='responsible_manager',
            field=models.ManyToManyField(to='backoffice.Manager'),
        ),
        migrations.AddField(
            model_name='company',
            name='subscription',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='backoffice.subscription'),
        ),
        migrations.CreateModel(
            name='InterviewSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.PositiveSmallIntegerField(blank=True, default=1)),
                ('time', models.TimeField(blank=True, default='08:00 AM', max_length=300)),
                ('is_active', models.BooleanField(default=True)),
                ('responsible_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.manager')),
            ],
            options={
                'unique_together': {('responsible_manager', 'day', 'time')},
            },
        ),
    ]
