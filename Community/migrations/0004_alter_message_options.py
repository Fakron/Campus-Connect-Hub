# Generated by Django 4.2.7 on 2024-03-31 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Community', '0003_alter_room_options_room_participant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
    ]