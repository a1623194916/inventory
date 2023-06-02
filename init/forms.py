from django.contrib.auth.forms import UserCreationForm  # 导入系统内置的表单，用于继承
from django.contrib.auth.models import User  # 导入系统的user模型，此处因为我用的就是系统自带的
from django import forms  # 导入表单模块


class usercreation(UserCreationForm):
    email = forms.EmailField(required=False, label='邮箱')  # 定义新字段
    username = forms.CharField(required=True, label='用户名')  # 定义新字段

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_superuser')  # 字段顺序
        error_messages = {  # 设置错误信息
            'username': {
                'required': '用户名不能为空',
                'max_length': '用户名最长不超过150个字符',
                'unique': '用户名已存在',
            },
        }
        help_texts = {
            'username': '用户名最长不超过150个字符a',
        }
        labels = {
            'username': '用户名',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名a'}),
        }
