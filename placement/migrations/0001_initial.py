# Generated by Django 4.1.5 on 2023-03-17 17:42

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import placement.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='signup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(default='', max_length=20, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='company_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=20)),
                ('Total_no_of_Positions', models.CharField(default='', max_length=10)),
                ('job_type', models.CharField(choices=[('1-months-internship', '1-Months Internship'), ('2-months-internship', '2-Months Internship'), ('3-months-internship', '3-Months Internship'), ('4-months-internship', '4-Months Internship'), ('5-months-internship', '5-Months Internship'), ('6-months-internship', '6-Months Internship'), ('7-months-internship', '7-Months Internship'), ('8-months-internship', '8-Months Internship'), ('9-months-internship', '9-Months Internship'), ('10-months-internship', '10-Months Internship'), ('11-months-internship', '11-Months Internship'), ('12-months-internship', '12-Months Internship'), ('full-time', 'Full-Time'), ('part-time', 'Part-Time')], default='full-time', max_length=50)),
                ('job_title', models.CharField(max_length=100)),
                ('job_description', models.CharField(default=' ', max_length=200)),
                ('location', models.CharField(blank=True, default='any', max_length=100, null=True)),
                ('skills_required', models.CharField(max_length=255)),
                ('salary', models.PositiveIntegerField()),
                ('monthly_annually', models.CharField(choices=[('p.m.', 'Monthly'), ('p.a.', 'Annual')], default='p.a', max_length=20, verbose_name='Monthly or Annual')),
                ('last_date_of_applying', models.DateField(validators=[placement.models.present_future_dates])),
                ('rounds_description', models.CharField(max_length=100)),
                ('date_of_interview', models.DateField(validators=[placement.models.present_future_dates])),
                ('reporting_time', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='studentData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=20)),
                ('last_name', models.CharField(default='', max_length=20)),
                ('ssc_percentage', models.CharField(max_length=10)),
                ('hsc_percentage', models.CharField(max_length=10)),
                ('graduation_semester_1_CGPA_or_percentage', models.CharField(max_length=10)),
                ('graduation_semester_2_CGPA_or_percentage', models.CharField(max_length=10)),
                ('graduation_semester_3_CGPA_or_percentage', models.CharField(max_length=10)),
                ('graduation_semester_4_CGPA_or_percentage', models.CharField(max_length=10)),
                ('graduation_semester_5_CGPA_or_percentage', models.CharField(max_length=10)),
                ('graduation_semester_6_CGPA_or_percentage', models.CharField(max_length=10)),
                ('overall_CGPA_or_percentage', models.CharField(default='', max_length=10)),
                ('skills', models.CharField(blank=True, default=' ', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='appliedStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applied_date', models.DateField(default=django.utils.timezone.now)),
                ('company', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='placement.company_details')),
                ('user', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'company')},
            },
        ),
    ]