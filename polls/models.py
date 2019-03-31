from django.db import models
import datetime
from django.utils import timezone
# https://docs.djangoproject.com/zh-hans/2.1/topics/db/models/#fields
class QManager(models.Manager):

    def add_one_question(self, text, date):
        '''添加一个问题'''

        question = super().create(question_text=text, pub_date=date)
        return question

    def get_one_question(self, text):
        question = self.get(question_text=text)
        return question


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):  # 给模型增加 __str__() 方法是很重要的，这不仅仅能给你在命令行里使用带来方便，Django 自动生成的 admin 里也使用这个方法来表示对象。
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    # 以下为了在admin页面展示用
    was_published_recently.admin_order_field = '-pub_date', # was_published_recently可排序，还可以跨表跨关系引用，如下：
    # author_first_name.admin_order_field = 'author__first_name'
    was_published_recently.boolean = True  # was_published_recently将显示为on/off的图标
    was_published_recently.short_description = 'Published recently?' # 列名

    objects = QManager()

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text