# from django.contrib import admin

# Register your models here.

from django.core.exceptions import ValidationError
from app01 import models
from django.shortcuts import render,redirect
from django import forms
from django.conf import settings
import hashlib
#将密码进行加密，对方法进行一个封装，然后调用使用
def md5(data_string):
    obj=hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()

def admin_list(request):
    '''管理员列表'''

    #检查用户是否登录，已登录，继续进入网站，为登录，跳转回登录界面
    #当用户发来请求，获取cookie随机字符串，拿着随机字符串看看session中是否存在
    info=request.session.get('info')
    if not info:
        return redirect('/login/')




    #搜索功能
    data_dict = {}
    search_data = request.GET.get('q', '')  # 有值和空值
    if search_data:
        data_dict['username__contains'] = search_data



    queryset=models.Admin.objects.filter(**data_dict)
    context={
        'queryset':queryset,
        'search_data': search_data
    }
    return render(request,'admin_list.html',context)

class  AdminModelForm(forms.ModelForm):

    confirm_password=forms.CharField(label='确认密码',widget=forms.PasswordInput(render_value=True))
    #render_value=True当密码不一致的时候，原来的密码不会清空
    class Meta:
        model = models.Admin
        # 展示字段内容第一种
        fields = ['username', 'password','confirm_password']
        widgets={'password':forms.PasswordInput(render_value=True)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加'class':'form-control'
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


    def clean_password(self):
        pwd=self.cleaned_data.get('password')
        return md5(pwd)
     #给确认的密码写一个钩子方法判断，让其与密码相同
    def clean_confirm_password(self):
        print(self.cleaned_data)
        pwd=self.cleaned_data.get('password')
        confirm=md5(self.cleaned_data.get('confirm_password'))
        if confirm!=pwd:
            raise ValidationError('密码不一致,请重新输入')
        return confirm #返回confirm表示当输入密码一致时，并将confirm返回，跟着pwd一起保存到数据库
def admin_add(request):
    title='新建管理员'
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'admin_add.html', {'form': form,'title':title})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        #判断数据是否合法，保存到数据库（第一种）
        # print(form.cleaned_data)
        #一般情况form内部会识别到用户提交的数据，将用户提交的数据保存到数据库form.save()
        form.save()
        return redirect('/admin_list/')
        # 校验失败并在页面上显示错误信息
    return render(request,'admin_add.html',{'form':form,'title':title})
class AdminEditModelForm(forms.ModelForm):
    class Meta:
        model=models.Admin
        fields=['username']
class AdminResetModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码',
                                       widget=forms.PasswordInput(render_value=True))
    class Meta:
        model=models.Admin
        fields=['password','confirm_password']
        widgets = {'password': forms.PasswordInput(render_value=True)}

    def clean_password(self):
        pwd=self.cleaned_data.get('password')
        md5_pwd=md5(pwd)
        #去数据库校验当前密码是否和当前输入的密码相同
        exists=models.Admin.objects.filter(id=self.instance.pk,password=md5_pwd)
        if exists:
            raise ValidationError('不能与以前的密码相同')
        return md5(pwd)
     #给确认的密码写一个钩子方法判断，让其与密码相同
    def clean_confirm_password(self):
        print(self.cleaned_data)
        pwd=self.cleaned_data.get('password')
        confirm=md5(self.cleaned_data.get('confirm_password'))
        if confirm!=pwd:
            raise ValidationError('密码不一致,请重新输入')
        return confirm #返回confirm表示当输入密码一致时，并将confirm返回，跟着pwd一起保存到数据库

def admin_edit(request,nid):
    if request.method == 'GET':
        row_object = models.Admin.objects.filter(id=nid).first()
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'admin_edit.html', {'form': form})

    row_object = models.Admin.objects.filter(id=nid).first()
    form = AdminEditModelForm(data=request.POST, instance=row_object)  # 更新到数据库
    if form.is_valid():
        form.save()
        return redirect('/admin_list/')

    return render(request, 'admin_edit.html', {'form': form})
def admin_delete(request,nid):
    # 删除
    models.Admin.objects.filter(id=nid).delete()

    return redirect('/admin_list/')

def admin_reset(request,nid):

    row_object=models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin_list/')
    title = '重置密码-{}'.format(row_object.username)
    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request,'admin_edit.html',{'form':form,'title':title})
    form = AdminResetModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return  redirect('/admin_list/')
    return render(request,'admin_reset.html',{'form':form})













