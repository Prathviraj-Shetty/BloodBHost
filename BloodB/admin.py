from django.contrib import admin
from BloodB.models import PERSON,DONATION,donates,RECEIVE,receives,STOCK
# Register your models here.
admin.site.register(PERSON)
admin.site.register(DONATION)
admin.site.register(donates)
admin.site.register(RECEIVE)
admin.site.register(receives)
admin.site.register(STOCK)
