from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# class CustomUser(AbstractUser):
#     image = models.ImageField(upload_to='images/' ,null=True,blank=True)

class Files(models.Model):
    file = models.ImageField(upload_to='im/', blank=True, null=True)

class CustomUser(AbstractUser):
    email = models.EmailField(blank=True , null = True)
    first_name = models.CharField(max_length=50 , blank = True , null = True)
    last_name = models.CharField(max_length=50 ,blank = True , null = True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    co_owner =models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE,null = True,blank = True)
    read_P = models.BooleanField(default = False)
    write_P = models.BooleanField(default = False)
    user1  = models.BooleanField(default = False)
    user2 = models.BooleanField(default = False)
 

            
class Projects(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default = -1)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name 

    class Meta:
        unique_together = ('user' ,'name')

class Modelnames(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default = -1)
    modelname = models.CharField(max_length=100)
    project = models.ForeignKey(Projects,on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.modelname

    class Meta:
        unique_together = ('user' ,'modelname')
