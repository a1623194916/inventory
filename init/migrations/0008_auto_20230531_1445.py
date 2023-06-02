# Generated by Django 3.2 on 2023-05-31 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('init', '0007_auto_20230531_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='check_sheet',
            name='In_supplier',
        ),
        migrations.AddField(
            model_name='check_sheet',
            name='in_num',
            field=models.IntegerField(default=0, verbose_name='入库数量'),
        ),
        migrations.AddField(
            model_name='check_sheet',
            name='out_num',
            field=models.IntegerField(default=0, verbose_name='出库数量'),
        ),
    ]