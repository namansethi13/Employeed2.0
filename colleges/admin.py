from django.contrib import admin
from .models import CollegeModel, CourseModel, CollegesCourses


admin.site.register(CollegeModel)
admin.site.register(CourseModel)
admin.site.register(CollegesCourses)