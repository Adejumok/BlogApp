# Generated by Django 4.1.3 on 2023-01-28 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_alter_comment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloginstance',
            name='subscriber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('6ca95aa2-137d-4e1f-809c-e1e2e9403bd7'), help_text='Unique ID for this particular comment', primary_key=True, serialize=False),
        ),
    ]