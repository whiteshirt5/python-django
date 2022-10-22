from django.shortcuts import render,redirect
def task_list(request):
    '''任务列表'''
    return render(request,'task_list.html')