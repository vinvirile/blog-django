from random import choices
from django.db import models

# Create your models here.
class Members(models.Model):
    id = models.AutoField(primary_key=True)
    # eid means Encrypted Identification which is the id, username, and the date encrypted all in one
    eid = models.CharField(max_length=128)
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('regular', 'Regular'),
        ('admin', 'Admin'),
        ('banned', 'Banned')
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="regular")
    activity = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username


class Blogs(models.Model):
    id = models.AutoField(primary_key=True)
    author_eid = models.CharField(max_length=128)
    eid = models.CharField(max_length=128, default="")
    title = models.CharField(max_length=84)
    image_url = models.TextField(max_length=2000)
    excerpt = models.CharField(max_length=500, default="")
    category = models.CharField(max_length=20, default="technology")
    blog_content = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_time = models.IntegerField(default=0)
    tags = models.CharField(max_length=255)

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted')
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    def save(self, *args, **kwargs):
        # Calculate read time based on average reading speed of 200 words per minute
        word_count = len(self.blog_content.split())
        self.read_time = max(1, round(word_count / 200))
        super().save(*args, **kwargs)
    
