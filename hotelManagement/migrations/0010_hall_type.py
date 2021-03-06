# Generated by Django 4.0.4 on 2022-07-23 19:48

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelManagement', '0009_remove_employee_image_employee_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hall_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('short_code', models.CharField(max_length=25)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('base_occupancy', models.IntegerField()),
                ('max_occupancy', models.IntegerField()),
                ('base_price', models.IntegerField()),
                ('amenities', models.ManyToManyField(blank=True, to='hotelManagement.amenity')),
                ('image', models.ManyToManyField(blank=True, to='hotelManagement.image')),
            ],
        ),
    ]
