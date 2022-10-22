from django.shortcuts import render,redirect
from app01 import models
from  django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
def depart_list(request):
    '''部门列表'''
    #去数据库获取所有的部门列表
    queryset=models.Department.objects.all()
    return render(request,'depart_list.html',{'queryset':queryset})

def depart_add(request):
    '''添加部门'''
    if request.method=='GET':
        return render(request, 'depart_add.html')

    #获取用户POST提交过来的数据(title输入为空)
    title=request.POST.get('title')
    #保存到数据库
    models.Department.objects.create(title=title)
    #重定向回部门列表
    return redirect('/depart_list/')

def depart_delete(request):
    #获取id
    nid = request.GET.get('nid')
    #删除
    models.Department.objects.filter(id=nid).delete()
    #重定向部门列表
    # 一般情况下会跳转到列表信息
    return redirect('/depart_list/')
#通过nid，传参保留原本的数据
def depart_edit(request,nid):
    '''修改部门'''
    if request.method == 'GET':
    #根据nid，获取他的数据[obj,]
        row_object=models.Department.objects.filter(id=nid).first()
        print(row_object.id,row_object.title)
        return render(request,'depart_edit.html',{'row_object':row_object})

    # 获取用户POST提交过来的修改的数据
    title = request.POST.get('title')
    # 保存到数据库
    models.Department.objects.filter(id=nid).update(title=title)
    # 重定向回部门列表
    return redirect('/depart_list/')

def user_list(request):
    queryset = models.UserInfo.objects.all()
    return render(request, 'user_list.html', {'queryset': queryset})

def user_add(request):
    '''添加用户(最原始方法)'''
    if request.method=='GET':
        #context表示从models拿数据过来
        context={
            'gender_choices':models.UserInfo.gender_choices,
            'depart_list':models.Department.objects.all()}
        return render(request, 'user_add.html', context)


    #获取用户POST提交过来的数据(title输入为空)
    user=request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('account')
    create_time = request.POST.get('create_time')
    depart_id = request.POST.get('depart_id')
    gender = request.POST.get('gender')




    # #获取用户提交的数据，将数据保存到数据库
    models.UserInfo.objects.create(name=user)
    models.UserInfo.objects.create(password=pwd)
    models.UserInfo.objects.create(age=age)
    models.UserInfo.objects.create(account=account)
    models.UserInfo.objects.create(create_time=create_time)
    models.UserInfo.objects.create(depart_id=depart_id)
    models.UserInfo.objects.create(gender=gender)

    #将添加的用户返回到用户列表，就是重定向回部门列表
    return redirect('/user_list/')



#----------------modelform示例（#基于modelform版本）-------------------
from  django import forms
class UserModelForm(forms.ModelForm):
    class Meta:
        model=models.UserInfo
        fields=['name','password','age','account','create_time','gender','depart_id']
        #通过Django后台进行前端输入框的显示：第一种方式
        # widgets={
        #     'name':forms.TextInput(attrs={'class':'form-control'}),
        #     'password': forms.TextInput(attrs={'class': 'form-control'}),
        #     'age': forms.TextInput(attrs={'class': 'form-control'}),
        # }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #循环找到所有的插件，添加'class':'form-control',让前端页面输入框中显示灰色底部提示标题
        for name,field in self.fields.items():
            field.widget.attrs={'class':'form-control','placeholder':field.label}

def user_model_form_add(request):
    if request.method=='GET':
        form=UserModelForm()
        return render(request,'user_model_form_add.html',{'form':form})

    #用户提交数据，数据校验。
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        #判断数据是否合法，保存到数据库（第一种）
        # print(form.cleaned_data)
        #一般情况form内部会识别到用户提交的数据，将用户提交的数据保存到数据库form.save()
        form.save()
        return redirect('/user_list/')
        # 校验失败并在页面上显示错误信息
    return render(request,'user_model_form_add.html',{'form':form})

def user_edit(request,nid):
    '''编辑用户'''
    #根据ID去数据库获取要编辑的那一行数据(对象)
    if request.method == 'GET':
        row_object=models.UserInfo.objects.filter(id=nid).first()
        form=UserModelForm(instance=row_object)
        return render(request,'user_edit.html',{'form':form})

    row_object = models.UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(data=request.POST,instance=row_object)#更新到数据库
    if form.is_valid():
        form.save()
        return redirect('/user_list/')

    return render(request, 'user_edit.html', {'form': form})

def user_delete(request,nid):
    
    # 删除
    models.UserInfo.objects.filter(id=nid).delete()
    # 重定向部门列表
    # 一般情况下会跳转到列表信息
    return redirect('/user_list/')


def pretty_list(request):
    # 搜索框关键字搜索
    data_dict = {}
    search_data = request.GET.get('q', '')  # 有值和空值
    if search_data:
        data_dict['mobile__contains'] = search_data
    res = models.PrettyNum.objects.filter(**data_dict)
    print(res)

    #此处添加循环是为了实现分页功能添加的数据使用
    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile='18697949601',price=10,level=1,status=1)
    page=int(request.GET.get('page',1))
    #第一种实现分页，实现每页显示10条数据
    # start=(page-1)*10
    # end=page*10
    #第二种可以进行定义变量，实现修改数字改变显示的数据条数
    page_num=10
    start = (page - 1) * page_num
    end = page * page_num





    #当数据过多时，在前端页面进行分页过于繁琐时，可以通过Django后台进行分页的一个循环
    page_str_list=[]

    # for i in range(1,21):
    #将page_string返回给前端页面展示，同时在下面的返回页面参数加上page_string
    #计算数据库有多少条数据，实现进行一个分页循环，其中循环21页显然是死代码，所以必须进行计算总条数
    total_count=models.PrettyNum.objects.filter(**data_dict).order_by('-level').count()

    #计算总页数， 将for i in range(1,21):的21替换成total_page_count+1
    total_page_count,div=divmod(total_count,page_num)#涉及到取余计算
    if div:
        total_page_count+=1

    for i in range(1, total_page_count+1):
        ele='<li><a href="?page={}">{}</a></li>'.format(i,i)
        page_str_list.append(ele)
        page_string=mark_safe(''.join(page_str_list))


    #select*from 表order by level desc;根据等级进行排序
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')[start:end]#次处加上[start:end]是实现上面的分页功能
    return render(request, 'pretty_list.html', {'queryset': queryset,'search_data':search_data,'page_string':page_string})


class PrettyModelForm(forms.ModelForm):
    #使用正则表达式对添加手机号码时进行一个验证，方法一：
    mobile=forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误')],
    )




    # # 通过构子的方法对添加手机号进行验证，第二种：
    # def clean_mobile(self):
    #     txt_mobile=self.cleaned_data['mobile']
    #
    #     if len(txt_mobile)!=11:
    #         #杨验证不通过
    #         raise ValidationError('格式错误')
    #     #验证通过，用户输入的值返回
    #     return txt_mobile




    class Meta:
        model=models.PrettyNum
        #展示字段内容第一种
        fields=['mobile','price','level','status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加'class':'form-control'
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    # 当添加手机号时，数据库已经存在该号码，可以通过构子的方法对添加手机号进行重复验证功能，
    # 但此处功能存在运行错误，问题还未解决
    # def clean_mobile(self):
    #     txt_mobile = self.cleaned_data['mobile']
    #     exists = models.PrettyNum.objects.filter(models=txt_mobile).exists()
    #
    #     if exists:
    #         # 验证不通过
    #         raise ValidationError('手机号码已经存在')
    #     # 验证通过，用户输入的值返回
    #     return txt_mobile



class PrettyEditModelForm(forms.ModelForm):


    #不修改手机号的情况下，但是使用此语句那么fields列表中必须加回原来的mobile
    # mobile=forms.CharField(disabled=True,label='手机号')
    #重新定义靓号编辑的类，与靓号增加的类进行一个区分使用
    class Meta:
        model=models.PrettyNum
        #展示字段内容方法一，当不展示手机号时可以进行去除，也可以使用语句mobile=forms.CharField(disabled=True,label='手机号')
        fields=['price','level','status']
        #展示字段第二种,表示展示全部
        # fields='__all__'
        #展示字段内容第三种，表示除了一下字段不展示，排除展示法
        # exclude=['level']
        #通过Django后台进行前端输入框的显示：第一种方式
        # widgets={
        #     'name':forms.TextInput(attrs={'class':'form-control'}),
        #     'password': forms.TextInput(attrs={'class': 'form-control'}),
        #     'age': forms.TextInput(attrs={'class': 'form-control'}),
        # }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #循环找到所有的插件，添加'class':'form-control'
        for name,field in self.fields.items():
            field.widget.attrs={'class':'form-control','placeholder':field.label}
#还可以使用上面的正则表达式验证手机号的方法
    # mobile = forms.CharField(
    #     label='手机号',
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    # )





def pretty_add(request):
    if request.method=='GET':
        form=PrettyModelForm()
        return render(request,'pretty_add.html',{'form':form})

    #用户提交数据，数据校验。
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        #判断数据是否合法，保存到数据库（第一种）
        # print(form.cleaned_data)
        #一般情况form内部会识别到用户提交的数据，将用户提交的数据保存到数据库form.save()
        form.save()
        return redirect('/pretty_list/')
        # 校验失败并在页面上显示错误信息
    return render(request,'pretty_add.html',{'form':form})

def pretty_edit(request,nid):
    if request.method == 'GET':
        row_object = models.PrettyNum.objects.filter(id=nid).first()
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {'form': form})

    row_object = models.PrettyNum.objects.filter(id=nid).first()
    form = PrettyEditModelForm(data=request.POST, instance=row_object)  # 更新到数据库
    if form.is_valid():
        form.save()
        return redirect('/pretty_list/')

    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):
    # 删除
    models.PrettyNum.objects.filter(id=nid).delete()
    # 重定向部门列表
    # 一般情况下会跳转到列表信息
    return redirect('/pretty_list/')

#订单管理使用到ajax知识

class OrderModelForm(forms.ModelForm):

    class Meta:
        model=models.Order
        #展示字段内容第一种
        fields=['oid','title','price','status','admin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加'class':'form-control'
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

def order_list(request):
    queryset = models.UserInfo.objects.all()
    return render(request, 'order_list.html', {'queryset': queryset})


def order_add(request):
    if request.method=='GET':
        form=OrderModelForm()
        return render(request,'order_add.html',{'form':form})

    #用户提交数据，数据校验。
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        #判断数据是否合法，保存到数据库（第一种）
        # print(form.cleaned_data)
        #一般情况form内部会识别到用户提交的数据，将用户提交的数据保存到数据库form.save()
        form.save()
        return redirect('/order_list/')
        # 校验失败并在页面上显示错误信息
    return render(request,'order_add.html',{'form':form})


















