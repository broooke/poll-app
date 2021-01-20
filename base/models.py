from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Poll(models.Model):
    question = models.CharField(max_length=100, unique=True)
    one_choice = models.CharField(max_length=30)
    two_choice = models.CharField(max_length=30)
    three_choice = models.CharField(max_length=30)
    one_choice_count = models.IntegerField(default=0)
    two_choice_count = models.IntegerField(default=0)
    three_choice_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

    @property
    def total(self):
        return self.one_choice_count + self.two_choice_count + self.three_choice_count
        
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    class Meta:
        unique_together = ("user", "poll")
        