from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Question
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.template import loader

# 模板系统统一使用点符号来访问变量的属性。在示例 {{ question.question_text }} 中，首先 Django 尝试对 question 对象使用字典查找（也就是使用 obj.get(str) 操作），如果失败了就尝试属性查找（也就是 obj.str 操作），结果是成功了。如果这一操作也失败的话，将会尝试列表查找（也就是 obj[int] 操作）


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list} # 将模板内的变量映射为 Python 对象。
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context) # render是上面的简化版本


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id) # 是上面的简化版本
    return render(request, 'polls/detail.html', {'question': question})
    # 也有 get_list_or_404() 函数，工作原理和 get_object_or_404() 一样，除了 get() 函数被换成了 filter() 函数。如果列表为空的话会抛出 Http404 异常。


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
