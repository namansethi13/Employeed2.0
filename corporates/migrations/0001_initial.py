# Generated by Django 4.0.6 on 2022-08-22 15:37

import accounts.managers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('colleges', '0001_initial'),
        ('accounts', '0003_delete_corporatemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorporateModel',
            fields=[
                ('baseuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Company Name')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address')),
                ('website', models.URLField(blank=True, max_length=255, null=True, verbose_name='Website')),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name_plural': 'corporates',
            },
            bases=('accounts.baseuser',),
            managers=[
                ('objects', accounts.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SkillModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=255, unique=True, verbose_name='Skill Name')),
            ],
            options={
                'verbose_name': 'skill',
                'verbose_name_plural': 'skills',
            },
        ),
        migrations.CreateModel(
            name='JobModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=255, verbose_name='Job Name')),
                ('job_description', models.TextField(verbose_name='Job Description')),
                ('eligibility', models.TextField(default='Open for all', verbose_name='Eligibilty')),
                ('post_it', models.CharField(choices=[('PRIVATE', 'Private'), ('POSTED', 'Posted'), ('FINISHED', 'Finished')], default='PRIVATE', max_length=10, verbose_name='Post It')),
                ('eligible_courses', models.ManyToManyField(related_name='job_courses', to='colleges.coursemodel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='corporates.corporatemodel')),
                ('skills', models.ManyToManyField(related_name='job_skills', to='corporates.skillmodel')),
            ],
            options={
                'verbose_name': 'job',
                'verbose_name_plural': 'jobs',
            },
        ),
    ]
