# Generated by Django 3.2.6 on 2021-12-04 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_post_date_posted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='pic',
        ),
        migrations.AddField(
            model_name='post',
            name='file',
            field=models.FileField(default='', upload_to='post'),
        ),
    ]
