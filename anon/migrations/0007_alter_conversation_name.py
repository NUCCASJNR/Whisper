# Generated by Django 5.0.8 on 2024-11-14 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("anon", "0006_conversation_user_pins"),
    ]

    operations = [
        migrations.AlterField(
            model_name="conversation",
            name="name",
            field=models.CharField(default="WHISPER", max_length=150),
        ),
    ]
