from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
#user authenticate
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.template import loader

from django.db.models import Q
#message
from django.contrib import messages
#form
from .forms import SignUpForm,ProfileForm,ApplicationForm
#models
from .models import Profile,Relationship,Message,Job,Applicant
#class view
from django.views.generic import ListView,DetailView

# Create your views here.

# def Index(request):
#     return render(request,"Profile/index.html")

def login_view(request):
    if request.method == 'POST':
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(User,username=username,password=password)
        
        if user is not None:
            login(request, user)
            return redirect("home")
            
        else:
            return redirect("login")
    else:
        context={
            "user":User
        }
        return render(request,"Profile/login.html",context)
    
def register_view(request):
    if request.method == "POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
        else:
            messages.info(request,"Fill in the details")
            
    else:
        
        form=SignUpForm()
        return render(request,"Profile/register.html",{"form":form})
    
def logout_view(request):
    logout(request)
    return redirect('login')

def User_profile_view(request):
    profile=Profile.objects.get(user=request.user)
    form=ProfileForm(request.POST or None,request.FILES or None,instance=profile)
    confirm=False
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm=True
    context={
        "profile":profile,
        "form":form,
        "confirm":confirm
    }
    return render(request,"Profile/Profile.html",context)
        
        
class ProfileListView(ListView):
    model=Profile
    context_object_name="profiles"
    
    def get_queryset(self):
        profiles=Profile.objects.exclude(user=self.request.user)
        return profiles
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        user=User.objects.get(username__iexact=self.request.user)
        profile=Profile.objects.get(user=user)
        
        context['profile']=profile
        send_by=Relationship.objects.filter(sender=profile)#we are the sender
        receive_by=Relationship.objects.filter(receiver=profile)#we are the receiver
        
        received_by=[]
        
        sended_by=[]
        
        for item in send_by:
            received_by.append(item.receiver.user)
        for item in receive_by:
            sended_by.append(item.sender.user)
        context['received_by']=received_by
        print("Received by:",received_by)
        context['sended_by']=sended_by
        print("sended_by",sended_by)
        
        return context
        
    
class ProfileDetailsView(DetailView):
    model=Profile
    template_name="Profile/detail.html"
    ##since i have not mentione  context_object_name over here so default 
    # name would be object(used in template)
    
    def get_object(self,slug=None):
        slug=self.kwargs.get('slug')
        profile=Profile.objects.get(slug=slug)
        return profile
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        user=User.objects.get(username__iexact=self.request.user)
        profile=Profile.objects.get(user=user)
        context['profile']=profile
        
        return context
    
 #login_required   
def invite_received(request):
    profile=Profile.objects.get(user=request.user)
    qs=Relationship.objects.invite_receive(profile)
    results=list(map(lambda x:x.sender,qs))
    isEmpty=False
    if len(results) == 0:
        isEmpty=True
    print(len(results))
    context={
        'results':results,
        'isEmpty':isEmpty,
    }
    return render(request,"Profile/notify.html",context)  
@login_required
def accept_invite(request):
    if request.method == 'POST':
        pk=request.POST.get('profile_pk')
        sender=Profile.objects.get(pk=pk)
        receiver=Profile.objects.get(user=request.user)
        
        rel=get_object_or_404(Relationship,sender=sender,receiver=receiver)
        
        if rel.status == 'send':
            rel.status ='accept'
            
            rel.save()
    return redirect('invites')

def reject_invite(request):
    if request.method == 'POST':
        pk=request.POST.get('profile_pk')
        sender=Profile.objects.get(pk=pk)
        receiver=Profile.objects.get(user=request.user)
        
        rel=get_object_or_404(Relationship,sender=sender,receiver=receiver)
        
        rel.delete()
    return redirect("invites")
def send_fr(request):
    if request.method == 'POST':
            pk=request.POST.get("profile_pk")
            sender=Profile.objects.get(user=request.user)
            receiver=Profile.objects.get(pk=pk)
            
            rel=Relationship.objects.create(sender=sender,receiver=receiver,status="send")

    
    return redirect("profile_list")

def remove_from_fr(request):
    if request.method == 'POST':
        pk=request.POST.get("profile_pk")
        sender=Profile.objects.get(user=request.user)
        receiver=Profile.objects.get(pk=pk)
        
        rel=Relationship.objects.filter(Q(sender=sender)& Q(receiver=receiver) | Q(sender=receiver) & Q(receiver=sender))
        
        rel.delete()
    return redirect("profile_list")
        
def search_name(request):
    if request.method == "POST":
        search=request.POST.get("search")
        print(search)
        person=Profile.objects.filter(Q(first_name__startswith=search)).exclude(user=request.user)
        print(person)
        context={
            "person":person,
            "search":search
        }
        
        return render(request,"Profile/search.html",context)
    
'''for showing received messages'''
@login_required
def Inbox(request):
    user=request.user
    profile=Profile.objects.get(user=user)
    #to gte messages
    #messages=Message.get_messages(user=user)
    #To see messages in Inbox recepient must be current user
    messages=Message.objects.filter(recepient__user=user)
    if messages:
        message=messages[0]
        
       ## active_direct=message['user']
        ##directs=Message.objects.filter(user__user=user,recepient=message['user'])
        directs=Message.objects.filter(recepient__user=user)
        directs.update(is_read=True)
    else:
        directs={}
        
        
    context={
        "user":profile,
        "messages":messages,
        ##"active_direct":active_direct,
        "directs":directs,
        
        
    }
    template=loader.get_template("Profile/inbox.html")
    return HttpResponse(template.render(context,request))
@login_required
def Directs(request,username):
    user=request.user
    messages=Message.get_messages(user=user)
    active_direct=username
    directs=Message.objects.filter(user=user)
    
    directs.update(is_read=True)
    
    context={
        "messages":messages,
        "active_direct":active_direct,
        "directs":directs
    }
    template=loader.get_template("Profile/inbox.html")
    return HttpResponse(template.render(context,request))
@login_required
def sendDirects(request):
    from_user=Profile.objects.get(user=request.user)
    body=request.POST.get('body')
    print(body)
    if request.method == 'POST':
        
        print("From:",from_user)
        profile=request.POST.get("to_user")
        
        receiver=Profile.objects.get(pk=profile)
        print(receiver)
        
        m=Message(
            user=from_user,
            sender=from_user,
            recepient=receiver,
            body=body,
            is_read=True
            
        )
        
        m.save()
        return redirect('inbox')
   
    else:
        return HttpResponseBadRequest()
'''for directly sending message'''  
def sendMessage(request,id):
    rec=Profile.objects.get(id=id)
    sen=Profile.objects.get(user=request.user)
   # b=f"Hello {rec}, I am {sen}"
    if request.method == "POST":
        b=request.POST.get("message_body")
        m=Message(user=rec,sender=sen,recepient=rec,body=b)
        m.save()
    
    context={
        "rec":rec,
        "sen":sen,
        
    }
    return render(request,"Profile/send_message.html",context)
    
@login_required
def delete_message(request,id):
    message=Message.objects.get(id=id)
    profile=Profile.objects.get(user=request.user)
    #particular_user=Message.objects.filter(Q(sender=message.sender)& Q(recepient=profile))
    
    if request.method=='POST':
        message.delete()
        return redirect("inbox")
    context={
        "message":message,
        
    }
    return render(request,"Profile/m_delete.html",context)
#for replying
@login_required
def reply(request,id):
       from_user=request.user
       profile=Profile.objects.get(user=id)
       sender=Profile.objects.get(user=request.user)
       if request.method=='POST':
           body=request.POST.get("body")
           m=Message(user=profile,sender=sender,recepient=profile,body=body)
           m.save()
           
       print("TO:",profile)
       context={
           "profile":profile,
       }
       return render(request,"Profile/message.html",context)
@login_required 
def message_reply(request):
    profile=Profile.objects.get(user=request.user)
    user=request.user
    directs=Message.objects.filter(sender__user=user)
    
    context={
        'profile':profile,
        'directs':directs,
    }   
    #add pagination
    return render(request,"Profile/message_reply.html",context)
@login_required
def listJob(request):
    jobs=Job.objects.all()
    context={
        'jobs':jobs
    }
    
    return render(request,"Profile/list_jobs.html",context)



''' its working but file is not getting uploaded'''



@login_required
def singleJob(request,id):
    job=Job.objects.get(id=id)
   
    
    form=ApplicationForm()
    if request.method == "POST":
        
        form=ApplicationForm(request.POST,request.FILES)
        #automatically add job and user(it is not working)
        if form.is_valid():
            f=form.save(commit=False)
            f.job=Job.objects.get(id=id)
            f.applicant=Profile.objects.get(user=request.user)
            f.save()
        
        
        
    else:
        form=ApplicationForm()
    #checking if the user has already applied or not
    applied=Applicant.objects.filter(Q(job__title=job) & Q(applicant__user=request.user))
    print(applied)
    b=False
    #return true if applied
    if applied:
        b=True
    else:
        b=False
        
    context={
        'job':job,
        'form':form,
        'b':b
        
    }
    
    return render(request,"Profile/job.html",context)

