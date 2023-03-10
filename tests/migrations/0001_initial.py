# Generated by Django 4.0.6 on 2022-08-22 15:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('corporates', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=255, verbose_name='Test Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('total_questions', models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(100)], verbose_name='Total Questions')),
                ('pass_percentage', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Pass Percentage')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('duration', models.PositiveIntegerField(verbose_name='Duration')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Datetime')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Datetime')),
                ('job_test', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='job_test', to='corporates.jobmodel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corporates.corporatemodel')),
            ],
            options={
                'verbose_name': 'test',
                'verbose_name_plural': 'tests',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='QuestionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=1000, verbose_name='Question')),
                ('A', models.CharField(max_length=255, verbose_name='A')),
                ('B', models.CharField(max_length=255, verbose_name='B')),
                ('C', models.CharField(max_length=255, verbose_name='C')),
                ('D', models.CharField(max_length=255, verbose_name='D')),
                ('answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1, verbose_name='Answer')),
                ('is_public', models.BooleanField(default=False, verbose_name='Is Public')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corporates.corporatemodel')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corporates.skillmodel')),
                ('test', models.ManyToManyField(related_name='tests_questions', to='tests.testmodel')),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
                'ordering': ['id'],
            },
        ),
    ]
