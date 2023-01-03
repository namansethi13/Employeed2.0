from django.contrib import admin
from .models import StudentModel, StudentTestModel, StudentTestQuestionsModel

admin.site.register(StudentModel)
admin.site.register(StudentTestModel)
admin.site.register(StudentTestQuestionsModel)