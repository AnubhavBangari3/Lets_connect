from django.db import models
from django.contrib.auth.models import User

#utils
from .utils import get_unicode
from django.template.defaultfilters import slugify

from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255,blank=True)
    email=models.EmailField(max_length=255)
    country=models.CharField(max_length=255)
    
    cover=models.ImageField(upload_to="profile_picture",default="avatar.png",blank=True)
    college=models.CharField(max_length=255)
    about=models.TextField(max_length=255,default="Nothing to write")
    
    friends=models.ManyToManyField(User, blank=True,related_name="connections")
    
    slug=models.SlugField(unique=True,blank=True)
    
    message=models.ManyToManyField(User,blank=True,related_name="inblox_message")
    
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    
    def get_connection(self):
        return self.friends.all().count()
    
    def __str__(self):
        return str(self.user.username)
    
    
    def get_absolute_url(self):
        return reverse('profile_detail',kwargs={
            "slug":self.slug
            })
    def get_posts(self):
        return self.profile_posts.all()
    def save(self,*args,**kwargs):
        ex=False
        if self.first_name and self.last_name:
            to_slug=slugify(str(self.first_name)+""+str(self.last_name))
            ex=Profile.objects.filter(slug=to_slug).exists()
            
            while ex:
                to_slug=slugify(to_slug+""+str(get_unicode()))
                ex=Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug=str(self.user)
        self.slug=to_slug
        super().save(*args,**kwargs)
 

choices=(
    ('send','send'),
    ('accept','accept')
    )   
class RelationshipManager(models.Manager):
    def invite_receive(self,receiver):
        qs=Relationship.objects.filter(receiver=receiver,status='send')
        return qs   
    
class Relationship(models.Model):
    sender=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="sender")
    receiver=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="receiver")
    status=models.CharField(max_length=10,choices=choices)
    objects=RelationshipManager()
    
    def __str__(self):
        return f"Sender:{self.sender} - Receiver- {self.receiver}"
 
choices_message=(('received','received'),('sended','sended'))   
class Message(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True,related_name="user_me")
    sender=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True,related_name="from_user")
    recepient=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True,related_name="to_user")
    body=models.TextField(max_length=250)
    created=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)
    
    def __str__(self):
        return f"Sender:{self.sender} :Receiver{self.recepient} ID:{self.id}."
    
    # def send_message(from_user,to_user,body):
    #     sender_message=Message(
    #         user=from_user,
    #         sender=from_user,
    #         recepient=to_user,
    #         body=body,
    #         is_read=True
    #     )
        
    #     sender_message.save()
    #     recepient_message=Message(
    #         user=to_user,
    #         sender=from_user,
    #         body=body,
    #         recepient=from_user
    #     )
        
    #     recepient_message.save()
    #     return sender_message
    def get_messages(user):
        users=[]  ##user__user means Message(user) calling Profile(user) Foreign key
        messages=Message.objects.filter(user__user=user).values('recepient').order_by('-created')
        for message in messages:
            users.append({
                'user':Profile.objects.get(pk=message['recepient']),
                
                
                })
        return users
    class Meta:
        ordering=['-created',]
    
#for jobs 

expe=(
    ('1','0'),
    ('2','1-5'),
    ('3','more than 5')
)

class Job(models.Model):
    company=models.CharField(max_length=200,blank=True,null=True)
    title=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    
    description=models.TextField()
    requirement=models.TextField()
    
    experience=models.CharField(choices=expe,max_length=200)
    filled=models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.title)
    
class Applicant(models.Model):
    job=models.ForeignKey(Job,on_delete=models.CASCADE,related_name="job_apply")
    applicant=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="applicant")
    about=models.TextField()
    resume=models.FileField()
    
    def __str__(self):
        return str(self.applicant)
    

    
    
    
    