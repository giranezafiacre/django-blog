# Generated by Django 3.2.6 on 2021-11-05 11:35

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_alter_post_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='created_by'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
