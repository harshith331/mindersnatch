from django.db import models
from datetime import datetime
# Create your models here.
class Config(models.Model):
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return "Start and End Time"

class option(models.Model):
    text=models.CharField(max_length=50)
    next_sit=models.IntegerField()

    def __str__(self):
        return self.text

class Situations(models.Model):
    situation_no= models.IntegerField() 
    image = models.ImageField(upload_to = 'images',default='images/level1.jpg')
    # audio = models.FileField(upload_to = 'audio',default='audios/default.mp3')
    text = models.TextField()
    option_1 = models.ForeignKey(option,related_name='option1',on_delete=models.CASCADE,default=1)
    option_2 = models.ForeignKey(option,related_name='option2',on_delete=models.CASCADE,default=1)
    option_3 = models.ForeignKey(option,related_name='option3',on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.text

