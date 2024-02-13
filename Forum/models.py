from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Question(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=10000)
    content = models.TextField(null=True,blank=True)
    # upvote = models.ManyToManyField(User,related_name="question_post")
    # downvote = models.c
    date_created = models.DateTimeField(default=timezone.now)

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

    def __str__(self):
        return '%s - %s' % (self.question.title,self.question.user)

    def get_absolute_url(self):
        return reverse("Questiondetail", kwargs={"pk": self.pk})
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

    
