# Generated by Django 3.2 on 2023-05-29 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('init', '0002_auto_20230529_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='Picture',
            field=models.ImageField(default='/static/logo1.png', null=True, upload_to='images', verbose_name='图片'),
        ),
    ]
