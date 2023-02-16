# Generated by Django 4.1.3 on 2023-01-28 15:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_bloginstance_subscriber_alter_comment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('018be668-feae-43ef-8a6a-6804f23b7547'), help_text='Unique ID for this particular comment', primary_key=True, serialize=False),
        ),
    ]