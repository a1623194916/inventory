from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from .models import Material, In_storage, Out_storage
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .models import Backup_form
import os
from django.core.management import call_command
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.http import HttpResponse
from django.urls import path
from django.utils import timezone
import os
import datetime
from django.contrib import messages


from django.utils.safestring import mark_safe

def dashboard(request):
    materials = Material.objects.all() #获取所有物料
    min_warning = '' #初始化最小库存警告
    max_warning = '' #初始化最大库存警告
    for material in materials:#遍历所有物料
        if material.Now_inventory < material.Min_inventory:
            min_warning=f'{material}库存不足,请及时补货'  #如果库存小于最小库存,则警告
        elif material.Now_inventory > material.Max_inventory:
            max_warning=f'{material}库存超出,不允许进货' 
    inventory_count = Material.objects.count()
    user = request.user
    firstname2 = '超级管理员' if user.is_superuser else '普通用户'
    context = {'inventory_count': inventory_count, 'username': user.username, 'firstname2': firstname2, 'min_warning':min_warning, 'max_warning':max_warning}
    return render(request, 'dashboard.html', context)#返回dashboard.html页面
 

def is403_view(request, exception):
    return render(request, '403.html', status=403)


def safeguard(request):
    if request.method == 'POST':
        action=request.POST.get('action')
        if action=='backup':
            #获取当前登录用户
            adminstrator=request.user
            B_number=Backup_form.objects.all().count()+1 #获取当前备份数
            current_time=datetime.datetime.now() #获取当前时间
            backup_filename = f'backup_{current_time.strftime("%Y%m%d%H%M%S")}_{adminstrator}_{B_number}.json'
            backup_path = os.path.join('backup', backup_filename)
            call_command('dumpdata', exclude=['auth.permission', 'contenttypes', 'init.Backup_form'],output=backup_path)    
            # 弹窗提示备份成功
            messages.success(request, '备份成功')
            # 生成备份记录
            Backup_form.objects.create(B_number=B_number, B_date=current_time, B_administrator=adminstrator, B_file=backup_filename)
    return render(request, 'safeguard.html')

from django.db.models.functions import Cast
from django.db.models import DateField
import xlwt
from django.http import HttpResponse
import datetime
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    username=request.user.username
    permissions=request.user.get_all_permissions()
    return render(request, 'index.html',context=  {'username': username,'permissions':permissions})

def monthly_report(request):
    # 获取当前月份和年份
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    if request.method == 'POST':
        action=request.POST.get('action')
        if action=='search':
            month=int(request.POST.get('month'))
            year=int(request.POST.get('year'))
    # 查询数据库以获取所有相关数据
    materials = Material.objects.annotate(now_date=Cast('Now_datetime', output_field=DateField())) \
                           .filter(now_date__year=year, now_date__month=month)
    in_storage = In_storage.objects.annotate(in_date=Cast('In_date', output_field=DateField())) \
                            .filter(in_date__year=year, in_date__month=month)
    # in_storage = In_storage.objects.filter(Mnumber__in=materials)
    # out_storage = Out_storage.objects.filter(Mnumber__in=materials)

    out_storage = Out_storage.objects.annotate(out_date=Cast('Out_date', output_field=DateField())) \
                                .filter(out_date__year=year, out_date__month=month)
    # 将数据传递给模板进行渲染
    context = {
        'materials': materials,
        'in_storages': in_storage,
        'out_storage': out_storage,
        'year': year,
        'month': month,
    }
    if request.method == 'POST':
        action=request.POST.get('action')
        if action=='export':
            return _extracted_from_monthly_report_21(materials, in_storage, out_storage,year,month)
    return render(request, 'month.html', context)



import os
def _extracted_from_monthly_report_21(materials, in_storage, out_storage,year,month):
    response = HttpResponse(content_type='application/vnd.ms-excel') #指定返回格式为excel，excel文件MINETYPE为application/vnd.ms-excel
    response['Content-Disposition'] = f'attachment;filename={year}-{month}-monthlyreport.xls' #指定返回文件名为入库单据
    wb = xlwt.Workbook(encoding='utf-8') #创建一个工作簿
    sheet1 = wb.add_sheet('物料库存')#创建一个工作表
    sheet2 = wb.add_sheet('入库记录')#创建一个工作表
    sheet3 = wb.add_sheet('出库记录')#创建一个工作表

    # 创建一个居中对齐的样式
    style = xlwt.XFStyle()
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    style.alignment = alignment
    font=xlwt.Font()
    font.name='宋体'
    font.bold=True
    font.height=20*11 #设置字体大小
    style.font=font

    # 将样式应用于单元格
    sheet1.write_merge(0, 0, 0, 8, '物料库存', style)
    sheet1.write(1, 0, '物料序号', style)
    sheet1.write(1, 1, '物料名字', style)
    sheet1.write(1, 2, '物料价格', style)
    sheet1.write(1, 3, '最大库存', style)
    sheet1.write(1, 4, '最小库存', style)
    sheet1.write(1, 5, '当前库存', style)
    sheet1.write(1, 6, '物料描述', style)
    sheet1.write(1, 7, '物料时间', style)
    sheet1.write(1, 8, '供应商', style)
    data_row = 2
    sheet2.write_merge(0, 0, 0, 5, '入库记录', style)
    sheet2.write(1, 0, '入库编号', style)
    sheet2.write(1, 1, '物料序号', style)
    sheet2.write(1, 2, '入库来源', style)
    sheet2.write(1, 3, '入库时间', style)
    sheet2.write(1, 4, '入库供应商', style)
    sheet2.write(1, 5, '入库库存', style)
    sheet3.write_merge(0, 0, 0, 5, '出库记录', style)
    sheet3.write(1, 0, '出库编号', style)
    sheet3.write(1, 1, '物料序号', style)
    sheet3.write(1, 2, '出库方式', style)
    sheet3.write(1, 3, '出库时间', style)
    sheet3.write(1, 4, '出库供应商', style)
    sheet3.write(1, 5, '出库库存', style)
    for obj in materials:
        # 创建一个居中对齐的样式
        style = xlwt.XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        style.alignment = alignment
        sheet1.write(data_row, 0, obj.Mnumber, style)
        sheet1.write(data_row, 1, str(obj.Mname), style)
        sheet1.write(data_row, 2, obj.Price, style)
        sheet1.write(data_row, 3, obj.Max_inventory, style)
        sheet1.write(data_row, 4, obj.Min_inventory, style)
        sheet1.write(data_row, 5, obj.Now_inventory, style)
        sheet1.write(data_row, 6, obj.Description, style)
        sheet1.write(data_row, 7, str(obj.Now_datetime), style)
        sheet1.write(data_row, 8, obj.Supplier, style)   
        data_row = data_row + 1


    data_row = 2
    for obj in in_storage:
        # 创建一个居中对齐的样式
        style = xlwt.XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        style.alignment = alignment
        sheet2.write(data_row, 0, obj.In_number, style)
        sheet2.write(data_row, 1, str(obj.Mnumber), style)
        sheet2.write(data_row, 2, obj.Source, style)
        sheet2.write(data_row, 3, str(obj.In_date), style)
        sheet2.write(data_row, 4, obj.In_supplier, style)
        sheet2.write(data_row, 5, obj.In_inventory, style)
        data_row = data_row + 1


    data_row = 2
    for obj in out_storage:
        # 创建一个居中对齐的样式
        style = xlwt.XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        style.alignment = alignment
        sheet3.write(data_row, 0, obj.Out_number, style)
        sheet3.write(data_row, 1, str(obj.Mnumber), style)
        sheet3.write(data_row, 2, obj.Out_way, style)
        sheet3.write(data_row, 3, str(obj.Out_date), style)
        sheet3.write(data_row, 4, obj.Out_supplier, style)
        sheet3.write(data_row, 5, obj.Out_inventory, style)
        data_row = data_row + 1
        
    wb.save(response)
    return response

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from .models import In_storage, Out_storage, Material,Check_sheet,Backup_form
from django.contrib.auth.models import Group, Permission


view_check_sheet = Permission.objects.get(codename='view_check_sheet')
add_in_storage = Permission.objects.get(codename='add_in_storage')
view_in_storage = Permission.objects.get(codename='view_in_storage')
add_material = Permission.objects.get(codename='add_material')
view_material = Permission.objects.get(codename='view_material')
add_out_storage = Permission.objects.get(codename='add_out_storage')
view_out_storage = Permission.objects.get(codename='view_out_storage')
# 获取名为norml_group1的分组
group = Group.objects.get(name='norml_group1')
# 将view_material和view_article权限授予norml_group1分组
group.permissions.add(add_in_storage, view_in_storage, add_material, view_material, add_out_storage, view_out_storage)

def register(request):
    if request.method == 'POST':
                # 获取所有权限
        permissions = Permission.objects.all()

        # 打印所有权限的名称和代码名
        for permission in permissions:
            print(f'{permission.name}: {permission.codename}')
        form = UserCreationForm(request.POST) #创建一个表单对象
        if form.is_valid(): #判断表单数据是否合法
            form.save() #将表单数据保存到数据库
            # 设置为is_staff=True，允许登录admin后台
            user = User.objects.get(username=form.cleaned_data['username'])
            user.is_staff = True
            # 将用户添加到norml_group1分组
            user.groups.add(group)
            user.save()
            messages.success(request, '注册成功！')
            return redirect('admin:index') #跳转到登录页面
        else:
            #如果数据不合法，返回具体的错误信息
            errors = form.errors.as_data()
            for field, errors in errors.items():
                for error in errors:
                    message = f"{field}: {error.message}"
                    # 使用JavaScript的alert()函数显示错误信息
                    return HttpResponse(f"<script>alert('{message}');window.history.back();</script>")
            print(form.errors)
    else:
        form = UserCreationForm() #创建一个表单对象
    return render(request, 'register.html', {'form': form}) #创建一个表单对象
