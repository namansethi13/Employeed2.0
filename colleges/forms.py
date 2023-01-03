from django import forms
from .models import CourseModel
from .validators import validate_file_size
from django.core.validators import FileExtensionValidator


class AddCourceForm(forms.Form):
    """
    Form for selection a course form available course in the Database
    """
    # COURSE_OPTIONS = ()
    COURSE_OPTIONS = CourseModel.get_course_choice_options()
    course_options = forms.MultipleChoiceField(choices=COURSE_OPTIONS, required=False, widget={})


class UploadCsvForm(forms.Form):
    """
    Upload csv file
    """
    course_id = forms.CharField(widget=forms.HiddenInput())
    csv_file = forms.FileField(
        allow_empty_file=False,
        required=True,
        validators=[
            validate_file_size, 
            FileExtensionValidator(allowed_extensions=['csv'])
        ]
    )



