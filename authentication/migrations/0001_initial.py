# Generated by Django 4.2.4 on 2025-01-03 12:21

import datetime
from django.conf import settings
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
            name='User',
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
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('profile_picture', models.FileField(blank=True, null=True, upload_to='profilepictures/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='EmailPhoneVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('otp', models.CharField(max_length=6)),
                ('otp_expiry', models.DateTimeField(default=datetime.datetime(2025, 1, 3, 12, 26, 16, 968966, tzinfo=datetime.timezone.utc))),
                ('is_verified', models.BooleanField(default=False)),
                ('temp_token', models.CharField(blank=True, max_length=100, null=True)),
                ('temp_token_expiry', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'EmailPhoneVerification',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('remote_address', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('login_method_id', models.SmallIntegerField(choices=[(1, 'REGULAR'), (2, 'GOOGLE')], db_column='login_method', default=1)),
                ('browser_info', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('ip_address', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('os_info', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('timezone', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('location', models.JSONField(blank=True, default=None, null=True)),
                ('device_id', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_sessions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Session',
            },
        ),
    ]
