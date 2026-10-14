from django.db import models
from django.conf import settings

class ServiceRequest(models.Model):
    STATES=[("new","New"),("active","In progress"),("review","Awaiting approval"),("done","Completed")]
    PRIORITIES=[("normal","Normal"),("high","High"),("urgent","Urgent")]
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(max_length=140)
    client=models.CharField(max_length=100)
    description=models.TextField()
    priority=models.CharField(max_length=10,choices=PRIORITIES,default="normal")
    state=models.CharField(max_length=10,choices=STATES,default="new")
    due=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Activity(models.Model):
    request=models.ForeignKey(ServiceRequest,on_delete=models.CASCADE,related_name="activities")
    actor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
