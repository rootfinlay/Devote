# Generated by Django 4.1 on 2022-11-25 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_alter_voters_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='voters',
            name='timestamp',
            field=models.TimeField(auto_now_add=True, null=True, verbose_name='Timestamp'),
        ),
    ]
