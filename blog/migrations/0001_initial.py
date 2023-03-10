# Generated by Django 4.1.3 on 2023-01-28 12:48

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('blog_type', models.CharField(choices=[('F', 'Food'), ('T', 'Travel'), ('H', 'Health'), ('L', 'Lifestyle'), ('FB', 'Fashion & Beauty'), ('PH', 'Photography'), ('P', 'Personal'), ('DC', 'DIY Craft')], max_length=2)),
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='BlogType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a blog type(e.g. Celebrity Gist)', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Writer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'ordering': ['first_name'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('693f2b3a-687e-4400-ac14-cf3a63aa219a'), help_text='Unique ID for this particular comment', primary_key=True, serialize=False)),
                ('written_date', models.DateField(auto_now=True, null=True, verbose_name=datetime.datetime)),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.blog')),
            ],
            options={
                'ordering': ['written_date'],
            },
        ),
        migrations.CreateModel(
            name='BlogInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular blog instance acrosswhole blog website', primary_key=True, serialize=False)),
                ('imprint', models.CharField(max_length=200)),
                ('due_back', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('F', 'Freemium'), ('P', 'Pay-As-You-Go'), ('FU', 'Fixed Usage'), ('U', 'Unlimited')], default='F', help_text='Blog subscription', max_length=2)),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='blog.blog')),
            ],
            options={
                'ordering': ['due_back'],
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='writer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.writer'),
        ),
    ]
