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


