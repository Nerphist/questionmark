# Generated by Django 3.0 on 2019-12-23 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api_tests', '0004_auto_20191222_2103'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolvedTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('mark', models.IntegerField(default=0)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solved_tests', to='users.Student')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='api_tests.Test')),
            ],
            options={
                'db_table': 'solved_tests',
                'ordering': ['pk'],
                'abstract': False,
                'unique_together': {('test', 'student')},
            },
        ),
        migrations.CreateModel(
            name='SolvedQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='api_tests.Question')),
                ('solved_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solved_questions', to='analytics.SolvedTest')),
            ],
            options={
                'db_table': 'solved_questions',
                'ordering': ['pk'],
                'abstract': False,
                'unique_together': {('question', 'solved_test')},
            },
        ),
        migrations.CreateModel(
            name='SolvedAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='api_tests.Answer')),
                ('solved_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solved_answers', to='analytics.SolvedQuestion')),
            ],
            options={
                'db_table': 'solved_answers',
                'ordering': ['pk'],
                'abstract': False,
                'unique_together': {('solved_question', 'answer')},
            },
        ),
    ]
