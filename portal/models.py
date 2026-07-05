from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings
class Announcement(models.Model):
    content = models.TextField(verbose_name='Texts of advertisement')
    data_posted = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)


    def __str__(self):
        return self.content

class AnnouncementComments(models.Model):
    announcement = models.ForeignKey(Announcement,on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='comments')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


class MaintenanceRequest(models.Model):
    room_number = models.CharField(max_length=10,verbose_name="Rooms' number")
    user_name = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='repair_request')
    description = models.TextField(verbose_name='What is broken?')

    STATUS_CHOICES = [('new','New'),('in_progress','In progres'),('done','Done'),('none',None)]
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='new')

    date_added = models.DateTimeField(auto_now_add=True,verbose_name='Date')


    def __str__(self):
        return f'On demand {self.room_number}'


class CustomUser(AbstractUser):

    master = models.BooleanField(default=False)
    bewohner = models.BooleanField(default=True)
    leiterin = models.BooleanField(default=False)


class CleaningArea(models.Model):
    name_de = models.CharField(max_length=100,verbose_name='Name (DE)')
    name_ua = models.CharField(max_length=100,verbose_name='Назва (UA)')
    slug = models.SlugField(max_length=50,unique=True,help_text='Unic')

    def __str__(self):
        return f'{self.name_de} / {self.name_ua}'

    class Meta:
        verbose_name = 'Bereich'
        verbose_name_plural = 'Bereiche'


class CleaningDuty(models.Model):
    STATUS_CHOICES = [
        ('waiting','Warten(Очикування)'),
        ('done','Geputzt(Прибрано)'),
        ('failed','Nicht geputzt(Не прибрано)',),
    ]
    area = models.ForeignKey(CleaningArea,on_delete=models.CASCADE)

    date_start = models.DateField(verbose_name='Anfang der Woche')
    date_end = models.DateField(verbose_name='Ende der Woche')
    room_number = models.CharField(max_length=20,verbose_name='Room number')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='waiting',verbose_name='Status')

    def __str__(self):
        return f'Zimmer nummer {self.room_number} --> {self.area.name_de} ({self.date_start - self.date_end}) '


    class Meta:
        verbose_name = 'Duty'
        verbose_name_plural = 'Duties'
        ordering = ['date_start','date_end','area']







