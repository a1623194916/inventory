
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

![image](https://github.com/a1623194916/inventory/assets/43876825/8f2b9034-8c8b-46ca-b9e4-8466527f9836)
![image](https://github.com/a1623194916/inventory/assets/43876825/b70ed265-7ecc-4af6-b045-2d2cd7ea9f2d) 

 

## ***\*出库功能界面\****

![image](https://github.com/a1623194916/inventory/assets/43876825/5abe57a1-654d-4296-8b08-18dc36475af5)![输入图片说明]![image](https://github.com/a1623194916/inventory/assets/43876825/d2dc73ba-7035-48ec-9e0a-318cd7e08014)

## ***\*入库功能界面\****

![image](https://github.com/a1623194916/inventory/assets/43876825/41316e5b-490a-45c4-a6bc-4b50ba31e205)
![image](https://github.com/a1623194916/inventory/assets/43876825/0a0e87df-0ccc-4570-9d97-4d92af4b5838)

## ***\*物料盘点功能界面\****

![image](https://github.com/a1623194916/inventory/assets/43876825/17b669ff-015e-4ade-958a-55cf32e9fa5c)
![image](https://github.com/a1623194916/inventory/assets/43876825/211f5a29-defe-44cf-9ded-c9ecc40223bc)

 

 

## ***\*月底结存功能界面\****
![image](https://github.com/a1623194916/inventory/assets/43876825/bd45411f-d76f-4b05-9613-41c95082349d)

## ***\*安全管理功能界面\****

![image](https://github.com/a1623194916/inventory/assets/43876825/a8fa8cb9-17d4-44d5-aa93-4f0e161d27d2)![输入图片说明![image](https://github.com/a1623194916/inventory/assets/43876825/5651d61f-375a-4429-a782-33bcbee6a55b)
