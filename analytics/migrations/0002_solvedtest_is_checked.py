# Generated by Django 3.0 on 2019-12-27 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solvedtest',
            name='is_checked',
            field=models.BooleanField(default=False),
        ),
    ]
