# Generated by Django 3.2.13 on 2023-02-27 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='no_image.jpeg', upload_to='profile_images'),
        ),
    ]
