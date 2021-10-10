from django.shortcuts import render,redirect
from .models import Post,Like,Comment
from django.contrib.auth.decorators import login_required
from Profile.models import Profile

from django.views.generic.edit import UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PostForm,CommentForm

from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.

@login_required
def Index(request):
    posts=Post.objects.all()
    profile=Profile.objects.get(user=request.user)
    form=PostForm()
    comment_form=CommentForm()
    comment_added=False
    
    if request.method == 'POST':
        print("posting")
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=profile
            post.save()
            
            return redirect('home')
        else:
            pass
    form=PostForm()
    
    if "comment" in request.POST:
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            instance=comment_form.save(commit=False)
            instance.user=profile
            instance.post=Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            
            comment_form=CommentForm()
            comment_added=True
            return redirect('home')
            
        
    context={
        'posts':posts,
        'profile':profile,
        'form':form,
        'comment_form':comment_form,
        'comment_added':comment_added,
    }
    return render(request,'Profile/index.html',context)

class UpdatePost(LoginRequiredMixin,UpdateView):
    form_class=PostForm
    model=Post
    template_name="Posts/update_post.html"
    success_url=reverse_lazy("home")
    
    def form_valid(self,form):
        profile=Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None,"It's not your post")
    
class DeleteView(LoginRequiredMixin,DeleteView):
    
    model=Post
    template_name="Posts/delete.html"
    success_url=reverse_lazy("home")
    
    def get_object(self,*args,**kwargs):
        pk=self.kwargs.get('pk')
        obj=Post.objects.get(pk=pk)
        
        if obj.author.user==self.request.user:
            messages.warning(self.request,"Are you sure")
        else:
            messages.warning(self.request,"Not possible")
        return obj
            
    
    
@login_required
def like_view(request):
    user=request.user
    if request.method == "POST":
        post_id=request.POST.get('post_id')
        post_obj=Post.objects.get(id=post_id)
        profile=Profile.objects.get(user=user)
        
        if profile in post_obj.liked.all():
            print("Unliked")
            post_obj.liked.remove(profile)
        else:
            print("Liked")
            post_obj.liked.add(profile)
                                                        #name of app is Posts so we can say posts_id
        like,created=Like.objects.get_or_create(user=profile,posts_id=post_id)
        
        if not created:
            if like.value=='like':
                like.value='unlike'
            else:
                like.value='like'
        else:
            like.value=='like'
            post_obj.save();
            like.save()
        
       
            
    return redirect('home')
        
    
    
