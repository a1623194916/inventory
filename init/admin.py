from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from .forms import usercreation


# Register your models here.
# tasks/admin.py

# 修改标题
admin.site.site_header = 'kj的库存管理系统'
# 修改页脚
admin.site.site_title = 'kj的库存管理系统'
# 修改登录页标题
admin.site.index_title = 'kj的库存管理系统'



class customadmin(UserAdmin):
    # 要用admin.ModelAdmin，不能用useradmin否则字段没有改变我也不知道为什么
    form = usercreation  # 设置表单
    add_form = usercreation  # 设置添加表单
    list_display = ('username','first_name','last_name','email', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )


admin.site.unregister(User)  # 先取消注册原来的User，否则会提示重复注册
admin.site.register(User, customadmin)



from .models import Material,In_storage
from django.contrib import admin
from django.utils.safestring import mark_safe


class MaterialAdmin(admin.ModelAdmin):
    list_display=('Mnumber','image_img','Mname','Max_inventory','Min_inventory','Now_inventory','Description','Price','Supplier','Now_datetime','warning')
    list_filter=('Mnumber','Mname','Supplier','Now_datetime')
 
    def warning(self, obj):
        if(obj.Now_inventory and obj.Min_inventory and obj.Max_inventory):
            if obj.Now_inventory < obj.Min_inventory:
                return mark_safe('<span style="color:red">库存不足，请及时补货</span>')
            elif obj.Now_inventory > obj.Max_inventory:
                return mark_safe('<span style="color:red">库存超出，不允许入库</span>')
            else:
                return ''
        else:
            return ''
        
    
    warning.short_description = '库存警告'


    


admin.site.register(Material,MaterialAdmin)

import xlwt
from django.http import HttpResponse, JsonResponse
import datetime
class In_storageAdmin(admin.ModelAdmin):
    list_display=('In_number','Mnumber','In_date','In_supplier','In_inventory')
    list_filter=('Mnumber','In_date','In_supplier')
    actions = ['inreport']
    #根据已选中的记录生成入库单据，以excel的形式导出
    def inreport(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.ms-excel') #指定返回格式为excel，excel文件MINETYPE为application/vnd.ms-excel
        response['Content-Disposition'] = 'attachment;filename=instorage.xls' #指定返回文件名为入库单据
        wb = xlwt.Workbook(encoding='utf-8') #创建一个工作簿
        sheet = wb.add_sheet('入库单据')#创建一个工作表
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
        sheet.write_merge(0, 0, 0, 5, '入库单据', style)      
        sheet.write(1, 0, '入库单号', style)
        sheet.write(1, 1, '物料名字', style)
        sheet.write(1, 2, '入库日期', style)
        sheet.write(1, 3, '供应商', style)
        sheet.write(1, 4, '入库数量', style)
        data_row = 2
        for obj in queryset:
            # 创建一个居中对齐的样式
            style = xlwt.XFStyle()
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            style.alignment = alignment

            sheet.write(data_row, 0, obj.In_number, style)
            sheet.write(data_row, 1, str(obj.Mnumber), style)
            sheet.write(data_row, 2, obj.In_date.strftime('%Y-%m-%d'), style)
            sheet.write(data_row, 3, obj.In_supplier, style)
            sheet.write(data_row, 4, obj.In_inventory, style)
            data_row = data_row + 1
        wb.save(response)
        return response
    inreport.short_description = '生成入库单据'
    inreport.icon = 'fas fa-file-export'
    inreport.type = 'success'
    inreport.style = 'background-color: #00a65a; color: #fff; border-color: #008d4c;'
   




admin.site.register(In_storage,In_storageAdmin)

from .models import Out_storage as Ou
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class Out_storageAdmin(admin.ModelAdmin):
    list_display=('Out_number','Mnumber','Out_date','Out_supplier','Out_inventory','Out_way')
    list_filter=('Mnumber','Out_date','Out_supplier','Out_way')
    actions = ['outreport']

    def outreport(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.ms-excel') #指定返回格式为excel
        response['Content-Disposition'] = 'attachment;filename=outstorage.xls' #指定返回文件名为入库单据
        wb = xlwt.Workbook(encoding='utf-8') #创建一个工作簿
        sheet = wb.add_sheet('入库单据')#创建一个工作表
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
        sheet.write_merge(0, 0, 0, 5, '出库单据', style)      
        sheet.write(1, 0, '出库单号', style)
        sheet.write(1, 1, '物料名字', style)
        sheet.write(1, 2, '出库日期', style)
        sheet.write(1, 3, '消耗单位', style)
        sheet.write(1, 4, '出库数量', style)
        sheet.write(1, 5, '出库途径', style)
        data_row = 2
        for obj in queryset:
            # 创建一个居中对齐的样式
            style = xlwt.XFStyle()
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            style.alignment = alignment

            sheet.write(data_row, 0, obj.Out_number, style)
            sheet.write(data_row, 1, str(obj.Mnumber), style)
            sheet.write(data_row, 2, obj.Out_date.strftime('%Y-%m-%d'), style)
            sheet.write(data_row, 3, obj.Out_supplier, style)
            sheet.write(data_row, 4, obj.Out_inventory, style)
            sheet.write(data_row, 5, obj.Out_way, style)
            data_row = data_row + 1
        wb.save(response)
        return response
    outreport.short_description = '生成出库单据'
    outreport.icon = 'fas fa-file-export'
    outreport.type = 'success'
    outreport.style = 'background-color: #00a65a; color: #fff; border-color: #008d4c;'




admin.site.register(Ou,Out_storageAdmin)

from .models import Backup_form
import os
from django.core.management import call_command
from django.contrib import admin
from django.contrib import messages
from django.core.management import call_command
from django.http import HttpResponse
import os
import datetime
from django.contrib import messages
from django.utils.safestring import mark_safe
import codecs

class BackupAdmin(admin.ModelAdmin):
    list_display=('B_number','B_date','B_administrator','B_file')
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    actions=['restore','backup']
    # 数据库备份，只能以utf-8的编码方式加载数据库，但是我们包括中文，所以需要转换成utf-8的编码方式
    def restore(self, request, queryset):        
        if queryset.count() > 1:
            self.message_user(request, '只能选择一个进行备份', level=messages.ERROR)
        else:
            filename = f'{queryset[0].B_file}'

            with codecs.open(f'C:/Users/Kj/Desktop/inventory/backup/{filename}', 'r', 'gbk') as f:
                data = f.read()

                # 将gbk编码的文件转换成utf-8编码的文件
            with codecs.open(f'C:/Users/Kj/Desktop/inventory/backup/{filename}_utf8_file.json', 'w', 'utf-8') as f:
                f.write(data)
            call_command('loaddata', f'C:/Users/Kj/Desktop/inventory/backup/{filename}_utf8_file.json')
            self.message_user(request, '数据库恢复成功', level=messages.SUCCESS)

    def backup(self, request, queryset):
        pass
    backup.short_description = '备份数据库'
    restore.short_description = '恢复数据库'
    # 备份图标
    backup.icon = 'fas fa-file-archive'
    restore.icon = 'fas fa-file-import'
    # 备份类型
    backup.type = 'success'
    restore.type = 'danger'
    # 备份样式
    backup.style = 'background-color: #00a61a; color: #fff; border-color: #008d4c;'
    restore.style = 'background-color: #dd4b39; color: #fff; border-color: #d73215;'
    # 备份url,跳转到safeguads/下，path('safeguards/', views.safeguard, name='safeguard')
    backup.action_url = 'http://127.0.0.1:8000/safeguards/'
    restore.confirm = '确认恢复数据库吗？'
    backup.action_type = 1


    #点击删除，删除备份文件 ，未实现
    # def delete_queryset(self, request, queryset):
    #     super().delete_queryset(request, queryset)
    #     for obj in queryset:
    #         if os.path.exists(obj.B_file.path):
    #             print(obj.B_file.path)
    #             os.remove(obj.B_file.path)
    #             self.message_user(request, f'备份文件{obj.B_file}已删除', level=messages.SUCCESS)
    #         else:
    #             print('文件不存在')

        


admin.site.register(Backup_form,BackupAdmin)

from django.contrib import admin
from .models import Material




from .models import Check_sheet
from django.contrib import admin
from django.http import HttpResponse
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME


from simpleui.admin import AjaxAdmin

class CheckAdmin(AjaxAdmin): #要用AjaxAdmin 才行！！！！！！！！
    list_display=('Cnumber','Mnumber','C_date','Now_inventory','Actual_num')
    actions=('checks','export')
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def checks(self, request, queryset):
        
        post=request.POST 
        # c_num=post.get('c_num')
        m_num=post.get('m_num')
        new_num=post.get('new_num')
        # 更改material模型中的库存数量
        material=Material.objects.get(Mnumber=m_num)
        initmaterial=material.Now_inventory
        material.Now_inventory=new_num
        #heck_sheet 模型中的 Mnumber 字段是一个外键字段，它引用了 Material 模型中的一个实例。因此，你需要将一个 Material 实例赋给 Mnumber 字段，而不能直接将一个数字赋给它。
        # 如果你直接将一个数字赋给 Mnumber 字段，Django 会引发 ValueError 异常，提示你必须将一个 Material 实例赋给它。
        Check_sheet.objects.create(Mnumber=material,Actual_num=new_num,Now_inventory=initmaterial,C_date=datetime.datetime.now())
        material.save()

        if post.get('_selected'):
            return JsonResponse(data={
                'status': 'success',
                'msg': '盘点完成'
            })
    checks.layer ={
        'title': '盘点',
        'tips': '请输入盘点的物料编号/名称，与实际盘点数量',
                    'confirm_button': '确认提交',
                    'cancel_button': '取消',

        'params': [
            {
            # 这里的type 对应el-input的原生input属性，默认为input
            'type': 'input',
            # key 对应post参数中的key
            'key': 'm_num',
            # 显示的文本
            'label': '物料编号',
            # 为空校验，默认为False
            'require': True,
            
        },
       
          {
            'type': 'number',
            'key': 'new_num',
            'label': '实际数量',
            # 设置默认值
            'value': 0,
            'require': True,
        },]
    }

    checks.icon = 'fas fa-check'
    checks.type = 'success'
    checks.style = 'background-color: #00a65a; color: #fff; border-color: #008d4c;'


    def export(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.ms-excel') #指定返回格式为excel
        response['Content-Disposition'] = 'attachment;filename=check.xls' #指定返回文件名为入库单据
        wb = xlwt.Workbook(encoding='utf-8') #创建一个工作簿
        sheet = wb.add_sheet('盘点报表')#创建一个工作表
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
        sheet.write_merge(0, 0, 0, 4, '盘点报表', style)      
        sheet.write(1, 0, '盘点序号', style)
        sheet.write(1, 1, '物料序号', style)
        sheet.write(1, 2, '盘点日期', style)
        sheet.write(1, 3, '初始库存', style)
        sheet.write(1, 4, '实际数量', style)
        data_row = 2
        for obj in queryset:
            # 创建一个居中对齐的样式
            style = xlwt.XFStyle()
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            style.alignment = alignment

            sheet.write(data_row, 0, obj.Cnumber, style)
            sheet.write(data_row, 1, str(obj.Mnumber), style)
            sheet.write(data_row, 2, obj.C_date.strftime('%Y-%m-%d'), style)
            sheet.write(data_row, 3, obj.Now_inventory, style)
            sheet.write(data_row, 4, obj.Actual_num, style)
            data_row = data_row + 1
        wb.save(response)
        return response
    export.short_description = '导出盘点报表'
    export.icon = 'fas fa-file-excel'
    export.type = 'success'



        

    checks.short_description = '盘点'    
admin.site.register(Check_sheet,CheckAdmin)