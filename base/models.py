from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

    @property
    def total(self):
        set = self.choice_set.all()
        result = sum([i.votes for i in set])
        return result
    
class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    user = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL, blank=True)

    def __str__(self):
        return self.choice_text


        