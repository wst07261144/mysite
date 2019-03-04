from django.urls import path

from . import views

app_name = 'polls'  # 为路由添加命名空间，防止多个应用冲突
urlpatterns = [

    # name可以在模板里面 <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
    #                 <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>

    # # ex: /polls/
    # path('', views.index, name='index'),
    # # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),

    # 通用视图
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
