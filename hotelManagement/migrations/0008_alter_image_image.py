# Generated by Django 4.0.4 on 2022-07-21 19:26

from django.db import migrations, models
import hotelManagement.models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelManagement', '0007_imagefolder_remove_amenity_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=hotelManagement.models.upload_path),
        ),
    ]
