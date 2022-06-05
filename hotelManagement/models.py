from dataclasses import field
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm
from django import forms
from ckeditor.fields import RichTextField 

# Create your models here.
class Member(AbstractUser):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Amenity(models.Model):
    name = models.CharField(max_length=50)
    description = RichTextField(blank=True)
    active = models.BooleanField()
    image = models.ImageField(blank=True, null=True, upload_to='images/amenity/')

    def __str__(self):
        return self.name

    def serialize(self):
        url = ''
        if (self.image):
            url = self.image.url
        return {
            'pk': self.pk,
            'name': self.name,
            'description': self.description,
            'active' :self.active,
            'image' : url,
        }

class AmenityForm(ModelForm):
    class Meta:
        model = Amenity
        fields = '__all__'

class Room_Type(models.Model):
    title = models.CharField(max_length=50)
    short_code = models.CharField(max_length=25)
    description = RichTextField(blank=True)
    base_occupancy = models.IntegerField()
    max_occupancy = models.IntegerField()
    extra_bed = models.IntegerField()
    kids_occupancy = models.IntegerField()
    amenities = models.ManyToManyField(Amenity, blank=True)
    base_price = models.IntegerField()
    additional_person_price = models.IntegerField()
    extra_bed_price = models.IntegerField()
    image = models.ImageField(blank=True, null=True, upload_to='images/room_types/')

    def __str__(self):
        return self.title

    def serialize(self):
        url = ''
        if (self.image):
            url = self.image.url
        amenities = []
        if self.amenities.count() != 0:
            for x in self.amenities.all():
                if x.active:
                    amenities.append(x.pk)
        return {
            'pk': self.pk,
            'title': self.title, 
            'short_code': self.short_code,
            'description': self.description,
            'base_occupancy': self.base_occupancy,
            'max_occupancy': self.max_occupancy,
            'extra_bed' : self.extra_bed,
            'kids_occupancy': self.kids_occupancy,
            'amenities': amenities,
            'base_price': self.base_price,
            'additional_person_price': self.additional_person_price,
            'extra_bed_price': self.extra_bed_price,
            'image': url,
        }

def get_my_choices():
    available_choices = []
    for x in Amenity.objects.filter(active=True).all():
        available_choices.append((x.pk,x.name))
    return available_choices

class Room_TypeForm(ModelForm):

    amenities = forms.MultipleChoiceField(
        widget= forms.CheckboxSelectMultiple,
        choices= get_my_choices
    )
        
    class Meta:
        model = Room_Type
        fields = '__all__'

class Floor(models.Model):
    name = models.CharField(max_length=50)
    number = models.IntegerField(unique=True)
    description = RichTextField(blank=True)
    active = models.BooleanField()

    def __str__(self):
        return f'{self.number} - {self.name}'

    def serialize(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'number': self.number,
            'description': self.description,
            'active' :self.active,
        }

class FloorForm(ModelForm):
    class Meta:
        model = Floor
        fields = '__all__'

class Room(models.Model):
    room_type = models.ForeignKey(Room_Type, on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor,on_delete=models.CASCADE)
    room_number = models.IntegerField(unique=True)

    def serialize(self):
        return {
            'pk': self.pk,
            'room_type': self.room_type.title,
            'room_type_pk': self.room_type.pk,
            'floor': f'{self.floor.number} - {self.floor.name}',
            'floor_pk': self.floor.pk,
            'room_number': self.room_number,
        }

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'