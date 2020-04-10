from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

# Create your models here.
class Config(models.Model):
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)
    time = models.CharField(max_length=40,default='April 6, 2020 18:30:00')
    current_level=models.IntegerField(default=1)
    total_level=models.IntegerField(default=1)
    freeze_time = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return "Start and End Time"

class Player(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    current_sitn = models.IntegerField(default=1)
    email = models.CharField(max_length=100,blank=True)
    image = models.CharField(max_length=200,blank=True)
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=datetime.now)
    level=models.IntegerField(default=1)

    def __str__(self):
        return self.name

# @receiver(post_save,sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Player.objects.create(
#             user=instance, name=instance.username
#         )

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.player.save()

class option(models.Model):
    text=models.CharField(max_length=50)
    next_sit=models.IntegerField()
    end=models.BooleanField(default=False)
    message=models.CharField(max_length=200,default='na')
    image = models.ImageField(upload_to="images",default="https://source.unsplash.com/random")

    def __str__(self):
        return self.text

class Situation(models.Model):
    situation_no= models.IntegerField(unique=True) 
    image = models.ImageField(upload_to = 'images',default='images/level1.jpg')
    level=models.IntegerField(default=1)
    # audio = models.FileField(upload_to = 'audio',default='audios/default.mp3')
    sub=models.BooleanField(default=False)
    #for subjective sitn#
    next_sitn=models.IntegerField(default=1,help_text="Next situation number")
    ans=models.CharField(max_length=100,default='NA',help_text="Answer for the subjective question")
    #for objective sitn#
    text = models.TextField()
    option_1 = models.ForeignKey(option,related_name='option1',on_delete=models.CASCADE,blank=True,null=True)
    option_2 = models.ForeignKey(option,related_name='option2',on_delete=models.CASCADE,blank=True,null=True)
    option_3 = models.ForeignKey(option,related_name='option3',on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.situation_no) + " : " + self.text

    def splitAnswer(self):
        answers = self.ans
        answers = answers.strip().split(',')
        ans_array = []
        for answer in answers:
            ans_array.append(answer.strip().lower())
        print(ans_array)
        return ans_array

    def checkAnswer(self, player_ans):
        if self.sub:
            if player_ans is not None:
                answer = player_ans
                answer = answer.strip().lower()
                correct_ans = self.splitAnswer()
                for ans in correct_ans:
                    if answer == ans:
                        return True
            return False
        else:
            pass

class SituationTimer(models.Model):
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    situation = models.ForeignKey(Situation,on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime.now, null=True)
    end_time = models.DateTimeField(null=True)

    def start_epoch(self):
        return int(self.start_time.timestamp())

    def end_epoch(self):
        return int(self.end_time.timestamp())

    def timepassed(self):
        return (int(datetime.now().timestamp()) - int(self.start_time.timestamp()))

    def timedifference(self):
        diff=self.end_epoch() - self.start_epoch()
        if diff <= 300:
            return 1
        elif diff > 300 and diff <=600:
            return 2
        return 4