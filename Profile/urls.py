from django.urls import path
from .views import *
urlpatterns = [
    #path('home',Index,name="home"),
    path('',login_view,name="login"),
    path("register",register_view,name="register"),
    path("logout",logout_view,name="logout"),
    path("userprofile",User_profile_view,name="userprofile"),
    path('profilelist',ProfileListView.as_view(),name="profile_list"),
    path('profilelist/<slug>',ProfileDetailsView.as_view(),name="profile_detail"),
    path('invites_received',invite_received,name="invites"),
    path('invite/accept',accept_invite,name="accept"),
    path('invite/reject',reject_invite,name="reject"),
    path("send-fr",send_fr,name="fr"),
    path("reove_from_fr",remove_from_fr,name="remove_from_fr"),
    path("search_name",search_name,name="search_name"),
    path("Inbox",Inbox,name="inbox"),
    path("Inbox/Directs/<username>",Directs,name="directs"),
    path("Inbox/send",sendDirects,name="sendDirects"),
    path("Inbox/reply/<str:id>",reply,name="reply"),
    path("Inbox/message_reply",message_reply,name="message_reply"),
    path("Jobs",listJob,name="jobs"),
    path("Jobs/<str:id>",singleJob,name="job"),
    path("Inbox/<str:id>",delete_message,name="message"),
    path("profilelist/send/<str:id>",sendMessage,name="send_message")
    
]