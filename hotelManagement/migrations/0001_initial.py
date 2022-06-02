# Generated by Django 4.0.4 on 2022-06-01 19:51

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('active', models.BooleanField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/amenity/')),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('number', models.IntegerField(unique=True)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Room_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('short_code', models.CharField(max_length=25)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('base_occupancy', models.IntegerField()),
                ('max_occupancy', models.IntegerField()),
                ('extra_bed', models.IntegerField()),
                ('kids_occupancy', models.IntegerField()),
                ('base_price', models.IntegerField()),
                ('additional_person_price', models.IntegerField()),
                ('extra_bed_price', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/room_types/')),
                ('amenities', models.ManyToManyField(blank=True, null=True, to='hotelManagement.amenity')),
            ],
        ),
    ]
