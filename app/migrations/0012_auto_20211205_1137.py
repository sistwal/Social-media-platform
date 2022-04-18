# Generated by Django 3.2.6 on 2021-12-05 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_profile_dp'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dp',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.profile', to_field='dp'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dp',
            field=models.ImageField(blank=True, default='/static/img/avatar7.png', null=True, unique=True, upload_to='dp', verbose_name='dp'),
        ),
    ]