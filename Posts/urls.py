from django.urls import path
from .views import*

urlpatterns=[
   path('',Index,name="home"),
   path('like/',like_view,name="like"),
   path('<pk>/update',UpdatePost.as_view(),name="update_post"),
   path('delete/<pk>',DeleteView.as_view(),name="delete_post")
    ]