from django.contrib import admin
from .models import Question, Choice


# admin.site.register(Question)
# Register your models here.

class ChoiceInline(admin.TabularInline):  # admin.TabularInline关联对象以一种表格式的方式展示，显得更加紧凑  admin.StackedInline 按列显示
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # 以下是列表页面
    # 通常，Django只显示__str()__方法指定的内容。但是很多时候，我们可能要同时显示一些别的内容。要实现这一目的，可以使用list_display属性，它是一个由字段组成的元组，其中的每一个字段都会按顺序显示在“change list”页面上，代码如下
    # 根据你选择的过滤条件的不同，Django会在面板中添加不同的过滤选项。由于pub_date是一个DateTimeField，因此Django自动添加了这些选项：“Any date”, “Today”, “Past 7 days”, “This month”, “This year”。
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

    # 以下是表单页面
    # fields = ['pub_date', 'question_text']  # 为表单选择一个直观的排序方法

    # 将表单分为几个字段集，fieldsets 元组中的第一个元素是字段集的标题
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
