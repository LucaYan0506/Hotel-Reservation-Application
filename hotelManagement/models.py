from dataclasses import field
from django.db import models
from django.forms import ModelForm
from ckeditor.fields import RichTextField 

# Create your models here.
class Room_Type(models.Model):
    Title = models.CharField(max_length=50)
    Short_Code = models.CharField(max_length=25)
    Description = RichTextField(blank=True)
    Base_Occupancy = models.IntegerField()
    Max_Occupancy = models.IntegerField()
    Extra_Bed = models.IntegerField()
    Kids_Occupancy = models.IntegerField()
    Amenities = models.CharField(max_length=25)
    Base_Price = models.IntegerField()
    Additional_Person_Price = models.IntegerField()
    Extra_Bed_Price = models.IntegerField()

    def serialize(self):
        return {
            'pk': self.pk,
            'Title': self.Title, 
            'Short_Code': self.Short_Code,
            'Description': self.Description,
            'Base_Occupancy': self.Base_Occupancy,
            'Max_Occupancy': self.Max_Occupancy,
            'Extra_Bed' : self.Extra_Bed,
            'Kids_Occupancy': self.Kids_Occupancy,
            'Amenities': self.Amenities,
            'Base_Price': self.Base_Price,
            'Additional_Person_Price': self.Additional_Person_Price,
            'Extra_Bed_Price': self.Extra_Bed_Price,
        }

    def __str__(self):
        return self.Title


class Room_TypeForm(ModelForm):
    class Meta:
        model = Room_Type
        fields = '__all__'


class Floor(models.Model):
    Name = models.CharField(max_length=50)
    Number = models.IntegerField(unique=True)
    Description = RichTextField(blank=True)
    Active = models.BooleanField()

    def serialize(self):
        return {
            'pk': self.pk,
            'Name': self.Name,
            'Number': self.Number,
            'Description': self.Description,
            'Active' :self.Active,
        }

class FloorForm(ModelForm):
    class Meta:
        model = Floor
        fields = '__all__'