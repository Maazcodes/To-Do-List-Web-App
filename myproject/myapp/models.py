from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

TIME_CHOICES = (
    ('0', '00:00-01:00'),
    ('1', '01:00-02:00'),
    ('2', '02:00-03:00'),
    ('3', '03:00-04:00'),
    ('4', '04:00-05:00'),
    ('5', '05:00-06:00'),
    ('6', '06:00-07:00'),
    ('7', '07:00-08:00'),
    ('8', '08:00-09:00'),
    ('9', '09:00-10:00'),
    ('10', '10:00-11:00'),
    ('11', '11:00-12:00'),
    ('12', '12:00-13:00'),
    ('13', '13:00-14:00'),
    ('14', '14:00-15:00'),
    ('15', '15:00-16:00'),
    ('16', '16:00-17:00'),
    ('17', '17:00-18:00'),
    ('18', '18:00-19:00'),
    ('19', '19:00-20:00'),
    ('20', '20:00-21:00'),
    ('21', '21:00-22:00'),
    ('22', '22:00-23:00'),
    ('23', '23:00-00:00'),
   
)

class MyTasks(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="mytasks")
    task_id = models.AutoField(primary_key=True, verbose_name="ID")
    task_title = models.CharField(max_length=100, default="", help_text="The title of the task", verbose_name="Task Title", blank=False)
    task_desc = models.TextField(default="", help_text="The description of task", verbose_name="Task Description", blank=False)
    task_time_only = models.CharField(choices=TIME_CHOICES, default='0', max_length=50, verbose_name="Set task time")
    task_time = models.DateTimeField(default=timezone.now(), verbose_name="Task Date & Time")
    task_completed = models.BooleanField(default=False, verbose_name="Task Completed")
    task_date = models.CharField(default="", max_length=50)
    taskTime = models.TimeField("Task Time", blank=True, null=True)
    taskDate = models.DateField("Task Date", blank=True, null=True)
    
    def __str__(self):
        return self.task_title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
        
    # def save(self, request, *args, **kwargs):
    #     self.user = request.user
    #     super().save(self, request, *args, **kwargs)

    