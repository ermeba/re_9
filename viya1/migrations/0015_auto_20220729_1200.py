# Generated by Django 3.2.5 on 2022-07-29 09:00

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('viya1', '0014_auto_20220729_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='addressOf',
            field=models.CharField(default=datetime.datetime(2022, 7, 29, 9, 0, 48, 66913, tzinfo=utc), max_length=100),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(default=datetime.datetime(2022, 7, 29, 9, 0, 48, 63913, tzinfo=utc), max_length=100),
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(default=datetime.datetime(2022, 7, 29, 9, 0, 48, 64948, tzinfo=utc), max_length=20),
        ),
        migrations.AlterField(
            model_name='division',
            name='name',
            field=models.CharField(default=datetime.datetime(2022, 7, 29, 9, 0, 48, 63913, tzinfo=utc), max_length=20),
        ),
        migrations.AlterField(
            model_name='subdistrict',
            name='name',
            field=models.CharField(default=datetime.datetime(2022, 7, 29, 9, 0, 48, 65948, tzinfo=utc), max_length=20),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_project', models.CharField(default='name', max_length=300)),
                ('status_of_project', models.IntegerField(choices=[(1, 'completed'), (2, 'uncompleted')], default=0)),
                ('year_of_completion', models.CharField(default='year', max_length=300)),
                ('type_of_project', models.IntegerField(choices=[(1, 'Villa Complex'), (2, 'Apartment Complex')], default=0)),
                ('description', models.CharField(default='description', max_length=1000)),
                ('address', models.CharField(default='year', max_length=300)),
                ('phone_number', models.CharField(default='phone number', max_length=300)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='partner/')),
                ('website', models.CharField(default='link', max_length=100)),
                ('project', models.ForeignKey(default='No company', on_delete=django.db.models.deletion.CASCADE, related_name='partner_project', to='viya1.partner')),
            ],
        ),
    ]
