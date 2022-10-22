from django.shortcuts import render,redirect,HttpResponse
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from app01.admin import md5
from app01.code import check_code
from io import BytesIO
class LoginForm(forms.Form):
    username=forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True#表示用户名不能为空，是必填选项
    )
    # (render_value=True)表示在出现错误时不会置空，还会保留原来数据再输入框
    password=forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True#表示密码不能为空，是必填选项
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,
        required=True
    )

    #以下代码是将输入框中的文字样式以灰色字体显示出来
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加'class':'form-control'
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    #使用钩子方法对拿到的用户密码进行一个密文隐藏,接着在去数据库进行校验
    def clean_password(self):
        pwd=self.cleaned_data.get('password')
        return md5(pwd)



def login(request):
    '''登录'''
    if request.method=='GET':
        form=LoginForm
        return render(request,'login.html',{'form':form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        #验证成功，获取大用户名和密码
        # print(form.cleaned_data)

        #验证码的校验,此处pop是因为数据库里只有用户名和密码，不存在验证码，所以需要进行一个清除
        # 验证码是随机生成，需要到系统的内存文件进行比对校验

        user_input_code=form.cleaned_data.pop('code')
        code=request.session.get('image_code','')
        if code.upper()!=user_input_code.upper():
            form.add_error('code','验证码错误')
            return render(request, 'login.html', {'form': form})



        #去数据库校验用户名和密码是否正确,获取用户对象
        admin_object= models.Admin.objects.filter(**form.cleaned_data).first()
        #当获取的用户名为空时
        if not admin_object:
            #当用户名为空时，写一个错误提示,
            # form.add_error('uasername', '用户名或者密码错误')#会在用户名出提示错误信息
            form.add_error('password','用户名或者密码错误')#会在密码出提示错误信息
            return render(request,'login.html',{'form':form})

        #当用户名正确和密码正确时
        #网站会随机生成字符串，写到用户浏览器cookie中，在写入session中;
        #将需要存储的内容，ID或者名字存到session中，
        request.session['info']={'id':admin_object.id,'name':admin_object.username}

        #由于设置了验证码是60秒有效，需要对登录时间也进行一个设置，此处设置成7天免登录
        #session保存有7天时间  7天过后就会自动失效
        request.session.set_expiry(60*60*24*7)



        return redirect('/admin_list/')
        # 校验失败并在页面上显示错误信息
    return render(request,'login.html',{'form':form})

def logout(request):
    '''注销功能'''
    request.session.clear()
    return redirect('/login/')

def image_code(request):
    '''生成图片验证码'''
    #调用pillow函数，生成图片
    img,code_string=check_code()

    #写入到自己的session中（以便后面获取验证码再进行校验）
    request.session['image_code']=code_string
    #给验证码session设置一个60秒超时
    request.session.set_expiry(60)

    #创建一个内存文件将图片写入内存文件中，以便读取图片 不用在进行图片的打开以及读写操作
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())













