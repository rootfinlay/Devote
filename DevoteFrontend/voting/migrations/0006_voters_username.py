# Generated by Django 4.1 on 2022-11-27 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0005_voters_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='voters',
            name='username',
            field=models.CharField(default='test', max_length=64, verbose_name='Username'),
            preserve_default=False,
        ),
    ]
