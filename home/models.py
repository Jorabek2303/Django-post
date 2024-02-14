from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import Signal


class ProfileModel(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    user_email = models.CharField(max_length=120)
    user_image = models.ImageField(upload_to='userImg/')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
class CreatePostModel(models.Model):
    
    xabar = (
        ('yaxshi','yaxshi',),
        ('yomon','yomon',)
        )
    
    user = models.ForeignKey(ProfileModel,on_delete=models.CASCADE)
    turi = models.CharField(max_length = 10,choices=xabar)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='image/')
    information = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title


class CommentModel(models.Model):
    post_comment = models.CharField(max_length=200)
    post = models.ForeignKey(CreatePostModel, on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(ProfileModel,on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.post_comment
    
    
def CreateProfile(sender,instance,created, **kwargs):
    print(sender,instance,created)
    if created:
        ProfileModel.objects.create(user=instance)
    else:
        profile = ProfileModel.objects.get(user=instance)
        profile.user_email = instance.email
        profile.name = instance.first_name
        profile.save()
        
Signal.connect(post_save,CreateProfile,sender=User)