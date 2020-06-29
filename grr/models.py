from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class obj(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

class user_obj(models.Model):
    userfk = models.ForeignKey(User, models.PROTECT)
    objfk = models.ForeignKey(obj, models.PROTECT)

    def __str__(self):
        return (str(self.userfk.username) + ' ' + self.objfk.name)

class param(models.Model):
    unit = models.CharField(max_length = 50)

    def __str__(self):
        return self.unit

class sens(models.Model):
    type_choise = (
        ('Электроэнергия', 'Электроэнергия'),
        ('Холодная вода', 'Холодная вода'),
        ('Горячая вода', 'Горячая вода'),
    )
    name = models.CharField(max_length = 50)
    objfk = models.ForeignKey(obj, models.PROTECT)
    type = models.CharField(max_length = 50, choices=type_choise)
    paramfk = models.ForeignKey(param, models.PROTECT)

    def __str__(self):
        return (self.objfk.name + ': ' + self.name)

class values_sens(models.Model):
    tem = models.DecimalField(max_digits=11, decimal_places=4)
    dat = models.DateTimeField()
    sensfk = models.ForeignKey(sens, models.PROTECT)

    def __str__(self):
        return str(self.dat)
