# Generated by Django 3.1.7 on 2021-03-27 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0006_customer_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='avatar',
            field=models.ImageField(blank=True, default='profileimage.png', null=True, upload_to=''),
        ),
    ]
