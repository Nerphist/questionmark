# Generated by Django 3.0 on 2019-12-27 19:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api_tests', '0005_answer_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('uuid_token', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='api_tests.Test')),
            ],
            options={
                'db_table': 'anonymous_links',
                'ordering': ['pk'],
                'abstract': False,
            },
        ),
    ]
