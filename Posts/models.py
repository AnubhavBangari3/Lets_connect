from django.db import models
from Profile.models import Profile

# Create your models here.
class Post(models.Model):
    text=models.TextField()
    image=models.ImageField(upload_to="posts",blank=True,null=True)
    author=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="profile_posts")
    liked=models.ManyToManyField(Profile,blank=True,related_name="likes")
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.text[:30])
    
    def total_likes(self):
        return self.liked.all().count()
    
    #comment for the post 
    def comment_post(self):
        return self.comment_post.all().count()
    
    class Meta:
        ordering=['-created']
        
class Comment(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="comment_user")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comment_post")
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pk
        
choices=(('like','like'),('unlike','unlike'))

class Like(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="user_like")
    posts=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="profile_posts_like")
    value=models.CharField(choices=choices,default='like',max_length=8)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    
    def str(self):
        return f"{self.user}-{self.post}-{self.value}"