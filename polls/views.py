from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse


# 模板系统统一使用点符号来访问变量的属性。在示例 {{ question.question_text }} 中，首先 Django 尝试对 question 对象使用字典查找（也就是使用 obj.get(str) 操作），如果失败了就尝试属性查找（也就是 obj.str 操作），结果是成功了。如果这一操作也失败的话，将会尝试列表查找（也就是 obj[int] 操作）


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list} # 将模板内的变量映射为 Python 对象。
#     # template = loader.get_template('polls/index.html')
#     # return HttpResponse(template.render(context, request))
#     return render(request, 'polls/index.html', context) # render是上面的简化版本
#
#
# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     question = get_object_or_404(Question, pk=question_id) # 是上面的简化版本
#     return render(request, 'polls/detail.html', {'question': question})
#     # 也有 get_list_or_404() 函数，工作原理和 get_object_or_404() 一样，除了 get() 函数被换成了 filter() 函数。如果列表为空的话会抛出 Http404 异常。
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
#
#
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])  # request.POST 是一个类字典对象，让你可以通过关键字的
        # 名字获取提交的数据,Django 还以同样的方式提供 request.GET 用于访问 GET 数据 —— 但我们在代码中显式地使用 request.POST ，
        # 以保证数据只能通过 POST 调用改动。request.POST 的值永远是字符串。
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # TODO
        # reverse() 反向解析URL 调用将返回一个这样的字符串：'/polls/3/results/'
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# ------------------------下面采用通用视图的方式--------------------------------------------------
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question
from django.utils import timezone


class IndexView(generic.ListView):
    # 类似地，ListView 使用一个叫做 <app name>/<model name>_list.html 的默认模板；我们使用 template_name 来告诉 ListView 使用我们创
    # 建的已经存在的 "polls/index.html" 模板。
    # 在之前的教程中，提供模板文件时都带有一个包含 question 和 latest_question_list 变量的 context。对于 DetailView ， question 变量
    # 会自动提供—— 因为我们使用 Django 的模型 (Question)， Django 能够为 context 变量决定一个合适的名字。然而对于 ListView， 自动生成的
    # context 变量是 question_list。为了覆盖这个行为，我们提供 context_object_name 属性，表示我们想使用 latest_question_list。
    # 作为一种替换方案，你可以改变你的模板来匹配新的 context 变量 —— 这是一种更便捷的方法，告诉 Django 使用你想使用的变量名。
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    # 默认情况下，通用视图 DetailView 使用一个叫做 <app name>/<model name>_detail.html 的模板。在我们的例子中，它将使用
    # "polls/question_detail.html" 模板。template_name 属性是用来告诉 Django 使用一个指定的模板名字，而不是自动生成的默认名字

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
