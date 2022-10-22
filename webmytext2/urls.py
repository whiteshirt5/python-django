"""webmytext2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views,admin,task,upload,account

urlpatterns = [
    # path('admin/', admin.site.urls),
    #部门管理
    path('depart_list/', views.depart_list),
    path('depart_add/', views.depart_add),
    path('depart_delete/', views.depart_delete),
    #编辑部门保留原来数据，通过正则表达式<int:nid>进行，逻辑是通过获取ID参数，引入原本的部门名称数据
    path('depart/<int:nid>/edit/', views.depart_edit),
    #用户管理
    path('user_list/', views.user_list),
    path('user_add/', views.user_add),
    path('user_model_form_add/',views.user_model_form_add),
    path('user/<int:nid>/edit/', views.user_edit),
    path('user/<int:nid>/delete/', views.user_delete),
    #靓号管理
    path('pretty_list/', views.pretty_list),
    path('pretty_add/', views.pretty_add),
    path('pretty/<int:nid>/edit/', views.pretty_edit),
    path('pretty/<int:nid>/delete/', views.pretty_delete),
    #管理员的管理
    path('admin_list/', admin.admin_list),
    path('admin_add/',admin .admin_add),
    path('admin/<int:nid>/edit/',admin .admin_edit),
    path('admin/<int:nid>/delete/',admin .admin_delete),
    path('admin/<int:nid>/reset/',admin .admin_reset),

    #任务管理，基于Ajax功能的使用，仅用于学习Ajax使用
    path('task_list/', task.task_list),
    #订单管理--使用到Ajax知识
    path('order_list/', views.order_list),
    path('order_add/', views.order_add),


    #上传文件
    path('upload_list/', upload.upload_list),
    #登录功能
    path('login/', account.login),
    path('logout/', account.logout),
    path('image_code/', account.image_code),
]
