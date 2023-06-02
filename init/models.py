import datetime
from django.db import models

# Create your models here.
from django.forms import ValidationError
from django.utils.html import format_html


# class User(AbstractUser):
# create table Material--物料信息
# ( Mnumber varchar(10) primary key,--物料序号
#  Mname     varchar(10) not null,--名称
#   Max_inventory int   not null,--最大库存
#   Min_inventory int   not null,--最小库存
#   Now_inventory int   not null,--当前库存
#   Description varchar(100) ,--描述信息
#   Picture  image  ,--图片
#   Price    float  not null,--价格
#   Now_datetime datetime not null default getdate(),--当前时间
#   Supplier varchar(20) not null,--供货单位
# )
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.core.validators import MinValueValidator, MaxValueValidator

class Material(models.Model):
    Mnumber = models.CharField(max_length=10, primary_key=True,verbose_name='物料序号',unique=True)
    Mname = models.CharField(max_length=10, null=False,verbose_name='名称',unique=True)
    Max_inventory = models.IntegerField(null=False,verbose_name='最大库存',validators=[MinValueValidator(1)])
    Min_inventory = models.IntegerField(null=False,verbose_name='最小库存',validators=[MinValueValidator(1)]) #大于0
    Now_inventory = models.IntegerField(null=False,verbose_name='当前库存',validators=[MinValueValidator(0)])
    Description = models.CharField(max_length=100,verbose_name='描述信息')
    Picture = models.ImageField(upload_to='C:\\Users\\Kj\\Desktop\\inventory\\media\\images', default='/static/logo1.png',verbose_name='图片',null=True)
    Price = models.FloatField(null=False,verbose_name='价格')
    Now_datetime = models.DateTimeField(verbose_name='入库时间',default=datetime.datetime.now)
    Supplier = models.CharField(max_length=20,null=False,verbose_name='供货单位') 

    
    def clean(self):
        if self.Max_inventory < self.Min_inventory:
            raise ValidationError('最大库存不能小于最小库存')
    
    def image_img(self):
        if not self.Picture:
            return '无图片'
        return format_html(
            """<div><img src='{}' style='width:50px;height:50px;' ></div>""",
            self.Picture.url)
    image_img.short_description = '图片'

    def warning(self,obj):
        if obj.Now_inventory<obj.Min_inventory:
            return format_html('<span style="color:red;">库存不足,请及时补货</span>')
        elif obj.Now_inventory>obj.Max_inventory:
            return format_html('<span style="color:blue;">库存超出，不允许入库</span>')
    warning.short_description='库存警告'


    def __str__(self):
        return self.Mname

# create table In_storage--入库
# (In_number varchar(8)  primary key,--入库编号
#  Mnumber varchar(10) foreign key (Mnumber) references Material(Mnumber),--物料序号
#  Source  Varchar(8) not null,--来源途径
#  In_date datetime not null default getdate() ,--入库时间
#  In_supplier varchar(20) ,--供货单位
#  In_inventory int not null,--数量
# )
import uuid
class In_storage(models.Model):
    In_number = models.AutoField(primary_key=True, verbose_name='入库编号',unique=True)
    Mnumber = models.ForeignKey(Material, on_delete=models.CASCADE,to_field='Mnumber',verbose_name='物料',related_name='in_storage')
    Source = models.CharField(max_length=8, null=False,verbose_name='来源途径')
    In_date = models.DateTimeField(auto_now_add=True,verbose_name='入库时间')
    In_supplier = models.CharField(max_length=20,verbose_name='供货单位')
    In_inventory = models.IntegerField(null=False,verbose_name='数量',validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        material=self.Mnumber
        total=material.Now_inventory+self.In_inventory
        if total>material.Max_inventory:
            raise ValidationError('入库数量超过最大库存')
        material.Now_inventory+=self.In_inventory
        material.save()
        super(In_storage, self).save(*args, **kwargs) # 调用父类的方法，将数据保存到数据库中

    def __str__(self):
        return str(self.In_number)
    
    


# create table Out_storage--出库
# (out_number varchar(8)  primary key,--出库编号
#  Mnumber varchar(10) foreign key (Mnumber) references Material(Mnumber) ,--物料序号
#  Out_way  Varchar(8) not null,--来源途径
#  Out_date datetime  not null default getdate() ,--出库时间
#  Out_supplier varchar(20) not null,--消耗
#  Out_inventory int not null,--数量
# )

class Out_storage(models.Model):
    Out_number = models.AutoField(primary_key=True, verbose_name='出库编号')
    Mnumber = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='out_storage', to_field='Mnumber', verbose_name='物料序号')
    Out_way = models.CharField(max_length=8, null=False, verbose_name='去向途径')
    Out_date = models.DateTimeField(auto_now_add=True, verbose_name='出库时间')
    Out_supplier = models.CharField(max_length=20, null=False, verbose_name='消耗单位')
    Out_inventory = models.IntegerField(null=False, verbose_name='数量',validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        material=self.Mnumber
        total=material.Now_inventory+self.Out_inventory
        if total<material.Min_inventory:
            raise ValidationError('入库数量超过最大库存')
        material.Now_inventory-=self.Out_inventory
        material.save()
        super(Out_storage, self).save(*args, **kwargs) # 调用父类的方法，将数据保存到数据库中

    def __str__(self):
        return str(self.Out_number)

# create table Check_sheet--盘点表格
# (Cnumber varchar(8) primary key,--盘点序号
#  Mnumber varchar(10) foreign key (Mnumber) references Material(Mnumber),--物料序列
#  In_supplier varchar(20),--供货商
#  C_date datetime not null default getdate(),--盘点日期
#  Now_inventory int   not null,--当前库存
#  Actual_num  int not null  --实际数量
# )
class Check_sheet(models.Model):
    Cnumber = models.AutoField(primary_key=True,verbose_name='盘点序号')
    Mnumber = models.ForeignKey(Material, on_delete=models.CASCADE, to_field='Mnumber',verbose_name='物料序号',related_name='check_sheet')
    # In_supplier = models.CharField(max_length=20,verbose_name='供货商')
    C_date = models.DateTimeField(auto_now_add=True,verbose_name='盘点日期')
    Now_inventory = models.IntegerField(null=False,verbose_name='初始库存')
    Actual_num = models.IntegerField(null=False,verbose_name='实际数量')


    def __str__(self):
        return str(self.Cnumber)
    
# create table Backup_form--备份恢复表格
# (B_number int primary key,--备份序号
# B_administrator varchar(20) not null,--备份管理员
# B_date datetime not null default getdate()--备份时间
# )
class Backup_form(models.Model):
    B_number = models.AutoField(primary_key=True,verbose_name='备份序号')
    B_administrator = models.CharField(max_length=20,null=False,verbose_name='备份管理员')
    B_date = models.DateTimeField(auto_now_add=True,verbose_name='备份时间')
    B_file = models.CharField(max_length=100,null=False,verbose_name='备份文件',default='无')

    def __str__(self):
        return str(self.B_number)






