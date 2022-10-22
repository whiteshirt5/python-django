from django.db import models

# Create your models here.
class Admin(models.Model):
    '''管理员'''
    username=models.CharField(verbose_name='用户名',max_length=32)
    password=models.CharField(verbose_name='密码',max_length=64)

class Department(models.Model):
    '''部门表'''
    title=models.CharField(verbose_name='标题',max_length=32)
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    '''员工表'''
    name=models.CharField(verbose_name='姓名',max_length=16)
    password=models.CharField(verbose_name='密码',max_length=64)
    age=models.IntegerField(verbose_name='年龄')
    account=models.DecimalField(verbose_name='账户余额',max_digits=10,decimal_places=2,default=0)
    # '''入职时间'''
    # create_time=models.DateTimeField(verbose_name='入职时间')
    create_time = models.DateField(verbose_name='入职时间')#DateField表示只包含年月日不包括分秒

    #当员工表和部门表进行关联时
    #无约束
    depart_id=models.BigIntegerField(verbose_name='所属部门')
    #1.有约束
    # #-to，与相应表关联
    # #-to_field,表中需要关联的哪一列
    # #2.django自动
    # #-写的depart
    # #-生成数据列 depart_id  理解：使用foreignkey时，django自动生成depart_id
    # # depart=models.ForeignKey(to='Department',to_fields='id')
    # #3.部门表被删除时，用户列表中所属部门ID要一并删除，用到级联删除on_delete
    # depart=models.ForeignKey(verbose_name='标题',to='Department',to_fields='id',on_delete=models.CASCADE)
    #3.1也可以在部门表删除后python manage.py makemigrations，让用户表的所属部门置为空值
    # # depart=models.ForeignKey(to='Department',to_fields='id',null=True,blank=True,on_delete=models.SET_NULL)
    # #在django中做约束
    gender_choices=(
        (1,'男'),
        (2,'女'),
    )
    gender=models.SmallIntegerField(verbose_name='性别',choices=gender_choices,null=True)

class PrettyNum(models.Model):
    '''靓号表'''
    mobile=models.CharField(verbose_name='手机号',max_length=32)
    #想要允许为空,null=True,blank=True
    price = models.IntegerField(verbose_name='价格',default=0)
    level_choices = (
        (1,'1级'),
        (2,'2级'),
        (3,'3级'),
        (4,'4级'),
    )
    level=models.SmallIntegerField(verbose_name='级别',choices=level_choices,default=1)

    status_choices = (
        (1,'已占用'),
        (2,'未占用'),
    )
    status=models.SmallIntegerField(verbose_name='状态',choices=status_choices,default=2)

class Order(models.Model):
    '''订单--使用ajax知识'''
    oid=models.CharField(verbose_name='订单号',max_length=64)
    title = models.CharField(verbose_name='名称', max_length=64)
    price=models.IntegerField(verbose_name='价格')
    status_choices=(
        (1,'待支付'),
        (2,'已支付'),
    )
    status=models.SmallIntegerField(verbose_name='状态',choices=status_choices,default=1)
    admin=models.ForeignKey(verbose_name='管理员',to='Admin',on_delete=models.CASCADE)










