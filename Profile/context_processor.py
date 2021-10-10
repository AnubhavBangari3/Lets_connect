from .models import Profile,Relationship,Message

def invitations_no(request):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user=request.user)
        no=Relationship.objects.invite_receive(profile).count()
        return {"no":no}
    return {}

def message_received(request):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user=request.user)
        re=Message.objects.filter(recepient=profile).count()
        return {"re":re}
    return {}
        