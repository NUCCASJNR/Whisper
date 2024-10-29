# Generated by Django 5.0.8 on 2024-10-29 16:57

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("anon", "0003_conversation"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="message",
            options={"ordering": ["created_at"]},
        ),
        migrations.RenameField(
            model_name="message",
            old_name="recipient",
            new_name="receiver",
        ),
        migrations.RemoveField(
            model_name="conversation",
            name="message",
        ),
        migrations.RemoveField(
            model_name="message",
            name="is_read",
        ),
        migrations.AddField(
            model_name="conversation",
            name="participants",
            field=models.ManyToManyField(
                related_name="conversations", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="conversation",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to="anon.conversation",
            ),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name="conversation",
            table="conversatiions",
        ),
        migrations.CreateModel(
            name="GroupMessage",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("content", models.TextField()),
                (
                    "conversation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="group_messages",
                        to="anon.conversation",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_group_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "group_messages",
                "ordering": ["created_at"],
            },
        ),
    ]