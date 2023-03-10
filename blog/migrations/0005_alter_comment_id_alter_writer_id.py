# Generated by Django 4.1.3 on 2023-01-30 16:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_comment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('3900f006-3d68-4de9-b85b-c5092f755d92'), help_text='Unique ID for this particular comment', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='writer',
            name='id',
            field=models.CharField(max_length=32, primary_key=True, serialize=False),
        ),
    ]
