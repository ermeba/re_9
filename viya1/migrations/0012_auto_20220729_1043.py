# Generated by Django 3.2.5 on 2022-07-29 07:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('viya1', '0011_auto_20220729_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='website',
            field=models.CharField(default='link', max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='addressOf',
            field=models.CharField(default=datetime.datetime(2022, 7, 29, 7, 43, 42, 68286, tzinfo=utc), max_length=100),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(default=datetime.datetime(2022, 7, 29, 7, 43, 42, 64286, tzinfo=utc), max_length=100),
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(default=datetime.datetime(2022, 7, 29, 7, 43, 42, 66286, tzinfo=utc), max_length=20),
        ),
        migrations.AlterField(
            model_name='division',
            name='name',
            field=models.CharField(default=datetime.datetime(2022, 7, 29, 7, 43, 42, 65287, tzinfo=utc), max_length=20),
        ),
        migrations.AlterField(
            model_name='subdistrict',
            name='name',
            field=models.CharField(default=datetime.datetime(2022, 7, 29, 7, 43, 42, 67287, tzinfo=utc), max_length=20),
        ),
    ]