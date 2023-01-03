from django.contrib import admin
from .models import CorporateModel, SkillModel, JobModel

admin.site.register(CorporateModel)
admin.site.register(SkillModel)
admin.site.register(JobModel)