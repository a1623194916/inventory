# Generated by Django 3.2 on 2023-06-01 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('init', '0010_auto_20230601_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check_sheet',
            name='Cnumber',
            field=models.AutoField(max_length=8, primary_key=True, serialize=False, verbose_name='盘点序号'),
        ),
    ]
