# Generated by Django 4.2.7 on 2024-03-31 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0005_category_question_categories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
