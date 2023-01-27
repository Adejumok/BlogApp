# Generated by Django 4.1.3 on 2023-01-27 22:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_blog_blog_type_alter_blog_id_alter_comment_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='writer',
            options={'ordering': ['first_name']},
        ),
        migrations.AlterField(
            model_name='blog',
            name='id',
            field=models.UUIDField(default=uuid.UUID('72c23d68-529b-49d8-b81d-40b60607cbbd'), help_text='Unique ID for this particular blog', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('a7046939-727d-46ee-98f6-73b9267b3745'), help_text='Unique ID for this particular comment', primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='BlogInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular blog across whole blog website', primary_key=True, serialize=False)),
                ('imprint', models.CharField(max_length=200)),
                ('due_back', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('F', 'Freemium'), ('P', 'Pay-As-You-Go'), ('FU', 'Fixed Usage'), ('U', 'Unlimited')], default='F', help_text='Blog subscription', max_length=2)),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='blog.blog')),
            ],
            options={
                'ordering': ['due_back'],
            },
        ),
    ]