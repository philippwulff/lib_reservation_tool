# Generated by Django 4.0 on 2022-01-01 22:20

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('full_name', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[a-zA-Z ]*$', 'Only alphabetic characters are allowed.')])),
                ('tum_id', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
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
            name='BackendError',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caused_by', models.TextField(verbose_name='Error cause')),
                ('info_text', models.TextField(verbose_name='Info')),
                ('at_time', models.DateTimeField(verbose_name='At datetime')),
            ],
        ),
        migrations.CreateModel(
            name='ReservationSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib_branch', models.CharField(choices=[('Stammgelände', 'Stammgelaende')], default='Stammgelände', max_length=50)),
                ('res_slot', models.CharField(choices=[('Morning', 'Morning'), ('Evening', 'Evening')], default='Morning', max_length=50)),
                ('pub_datetime', models.DateTimeField(verbose_name='Datetime published')),
                ('current_res_slot', models.TextField(default='', verbose_name='Date of last completed reservation')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation_app.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_datetime', models.DateTimeField(verbose_name='Datetime of reservation')),
                ('creation_datetime', models.DateTimeField(verbose_name='Datetime of creation')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation_app.reservationschedule')),
            ],
        ),
    ]
