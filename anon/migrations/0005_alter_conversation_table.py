# Generated by Django 5.0.8 on 2024-10-30 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("anon", "0004_alter_message_options_and_more"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="conversation",
            table="conversations",
        ),
    ]