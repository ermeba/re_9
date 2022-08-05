from django.contrib import admin
from .models import *
# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    list_display=['user','city','division','district','subdistrict']
    class Media:
        js=("admindrop/newajax.js",)

admin.site.register(Location,LocationAdmin)