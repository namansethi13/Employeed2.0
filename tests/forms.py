from dataclasses import fields
from .models import QuestionModel, TestModel
from django import forms

class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        fields=['question', 'A', 'B', 'C', 'D', 'answer','is_public','skill']

class TestForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = ['test_name', 'description', 'total_questions', 'pass_percentage', 'start_date', 'end_date', 'duration']
