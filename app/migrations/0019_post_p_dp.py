# Generated by Django 3.2.6 on 2021-12-05 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_remove_post_p_dp'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='p_dp',
            field=models.ImageField(blank=True, default='/static/img/avatar8.png', null=True, unique=True, upload_to='dp'),
        ),
    ]
