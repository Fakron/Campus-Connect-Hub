from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    def total_questions(self):
        return self.question_set.count()

    class Meta:
        verbose_name_plural = "Categories"

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=10000)
    content = models.TextField(null=True, blank=True)
    upvote = models.ManyToManyField(User, related_name="upvoted_questions", blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category)  # Change field name to 'category'
    tags = models.ManyToManyField('Tag', related_name='questions', blank=True)

    def __str__(self):
        return f'{self.user.username} - Question'

    def get_absolute_url(self):
        return reverse('Questiondetail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.upvote.count()



class Comment(models.Model):
    question = models.ForeignKey(Question,on_delete = models.CASCADE , related_name="comment")
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField(null=True,blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    upvote = models.ManyToManyField(User, related_name="upvoted_comments", blank=True)  # Upvote field for comments

    

    def __str__(self):
        return '%s - %s' % (self.question.title,self.question.user)

    def get_absolute_url(self):
        return reverse("Questiondetail", kwargs={"pk": self.pk})
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

    
