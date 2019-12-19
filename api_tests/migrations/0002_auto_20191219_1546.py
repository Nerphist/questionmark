# Generated by Django 3.0 on 2019-12-19 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_tests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='api_tests.Test'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together={('category', 'name')},
        ),
    ]
