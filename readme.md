
# 安装与使用说明

## 项目背景
项目名称：基于django的库存管理系统
项目版本：V 1.0
完成日期：2023年6月1日

## 系统环境
Windows10
MySQL
Python
Django版本3.2

## 配置文件

### 数据库配置
请根据上文数据库分析构建数据库基本表等，或根据文末附录源码进行数据库设计
settings.py
`DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "inventory",
        'USER': 'root',
        'HOST': 'localhost',
        'PASSWORD': '85224960',
        'PORT': '3306',
    }
}`


__init__.py
`import pymysql
pymysql.install_as_MySQLdb()`

### 虚拟环境配置
创建虚拟环境：
virtualenv venv
等待虚拟环境创建完成执行：
venv/bin/activate
然后安装项目所需安装包
pip install -r requirements.txt
安装过程如果发现错误，解决错误，直到所有文件安装完成。


# 功能简介
1. 注册与登录
2. 用户权限划分
2. 控制面板展示基本信息
3. 添加物料
4. 物料入库与出库，导出报表
5. 物料盘点，导出报表
6. 月底结存功能
7. 数据库备份与恢复


# 界面展示



## ***\*物料初始化界面\****

![输入图片说明](https://foruda.gitee.com/images/1685868162844280980/cfe66d92_12707783.png "屏幕截图")
![输入图片说明](https://foruda.gitee.com/images/1685868175653217907/5ab71715_12707783.png "屏幕截图")
 

 

## ***\*出库功能界面\****

![输入图片说明](https://foruda.gitee.com/images/1685868183422960180/e382b573_12707783.png "屏幕截图")
![输入图片说明](https://foruda.gitee.com/images/1685868190013367576/3bd31fcd_12707783.png "屏幕截图")

## ***\*入库功能界面\****

![输入图片说明](https://foruda.gitee.com/images/1685868198735624415/0f343085_12707783.png "屏幕截图")
![输入图片说明](https://foruda.gitee.com/images/1685868211382064135/6c839eb9_12707783.png "屏幕截图")

## ***\*物料盘点功能界面\****

![输入图片说明](https://foruda.gitee.com/images/1685868216856220946/d938c0e1_12707783.png "屏幕截图")
![输入图片说明](https://foruda.gitee.com/images/1685868224654026461/5c041df5_12707783.png "屏幕截图")
 

 

## ***\*月底结存功能界面\****
![输入图片说明](https://foruda.gitee.com/images/1685868234185306799/5278b42e_12707783.png "屏幕截图")


## ***\*安全管理功能界面\****

![输入图片说明](https://foruda.gitee.com/images/1685868244479046189/7fc96e84_12707783.png "屏幕截图")
![输入图片说明](https://foruda.gitee.com/images/1685868255776053475/92960e6a_12707783.png "屏幕截图")
