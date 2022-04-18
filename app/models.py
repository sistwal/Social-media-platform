from mimetypes import *
import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Max



# Create your models here.
class profile(models.Model):
    dp = models.ImageField(upload_to='dp', null=True, verbose_name='dp',default="/static/img/avatar7.png", blank = True, unique = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bio = models.TextField(max_length=150, verbose_name='bio', null=True, blank=False)
    def __str__(self):
        return str(self.user)

class Post(models.Model):
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to = "post", null=False, default="")
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    p_dp = models.ImageField(upload_to='dp', null=True,default="/static/img/avatar8.png", blank = True)
    tags = models.CharField(max_length=100, blank=True)
    post_time = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    comnt = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.user_name)
    
    def file_type(self):
        name, extension = os.path.splitext(self.file.name)
        if extension == '.jpg':
            return 'jpg'
        elif extension == '.JPG':
            return 'JPG'
        elif extension == '.jpeg':
            return 'jpeg'
        elif extension == '.JPEG':
            return 'JPEG'
        elif extension == '.mp4':
            return 'mp4'
        elif extension == '.MP4':
            return 'MP4'
        

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', default=None)
    message = models.CharField(max_length=1200, default="")
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
