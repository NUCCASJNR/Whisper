# Generated by Django 5.0.6 on 2024-05-11 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anon', '0004_plaintextmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encryptionkey',
            name='private_key',
            field=models.TextField(),
        ),
    ]
