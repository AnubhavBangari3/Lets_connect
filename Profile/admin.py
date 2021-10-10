from django.contrib import admin
from .models import Profile,Relationship,Message,Job,Applicant
# Register your models here.

admin.site.register(Profile)
admin.site.register(Relationship)
admin.site.register(Message)
admin.site.register(Job)
admin.site.register(Applicant)
