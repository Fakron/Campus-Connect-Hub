# Generated by Django 5.0.2 on 2024-02-14 12:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0002_question_upvote'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='downvote',
            field=models.ManyToManyField(blank=True, related_name='downvoted_questions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='upvote',
            field=models.ManyToManyField(blank=True, related_name='upvoted_questions', to=settings.AUTH_USER_MODEL),
        ),
    ]
