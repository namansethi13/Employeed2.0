from django import forms
from .models import JobModel

class JobForm(forms.ModelForm):
    class Meta:
        model = JobModel
        fields = ['job_name', 'job_description', 'eligibility', 'skills', 'eligible_courses']