# Generated by Django 3.2.6 on 2021-12-07 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='p_dp',
            field=models.ImageField(blank=True, default='/static/img/avatar8.png', null=True, upload_to='dp'),
        ),
    ]