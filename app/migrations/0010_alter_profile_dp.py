# Generated by Django 3.2.6 on 2021-12-04 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_profile_dp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dp',
            field=models.ImageField(default='/static/img/avatar7.png', null=True, upload_to='dp', verbose_name='dp'),
        ),
    ]
