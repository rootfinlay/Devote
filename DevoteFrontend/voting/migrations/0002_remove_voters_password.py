# Generated by Django 4.1 on 2022-11-25 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voters',
            name='password',
        ),
    ]