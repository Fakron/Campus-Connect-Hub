# Generated by Django 4.2.7 on 2024-04-01 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0008_tag_question_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='categories',
            new_name='category',
        ),
    ]