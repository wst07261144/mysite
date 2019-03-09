from django.contrib import admin
from .models import Question, Choice


# admin.site.register(Question)
# Register your models here.

class ChoiceInline(admin.TabularInline):  # admin.TabularInline关联对象以一种表格式的方式展示，显得更加紧凑  admin.StackedInline 按列显示
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # 以下是列表页面
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
