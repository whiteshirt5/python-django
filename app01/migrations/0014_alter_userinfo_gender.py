# Generated by Django 4.0 on 2022-10-08 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0013_prettynum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, '男'), (2, '女')], null=True, verbose_name='性别'),
        ),
    ]
