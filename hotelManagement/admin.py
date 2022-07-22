from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Room_Type)
admin.site.register(Floor)
admin.site.register(Amenity)
admin.site.register(Room)
admin.site.register(Employee)
admin.site.register(HousekeepingStatus)
admin.site.register(Housekeeping)
admin.site.register(Image)
admin.site.register(ImageFolder)