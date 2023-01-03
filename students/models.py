from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete
from colleges.models import CourseModel, CollegeModel
from corporates.models import SkillModel
from tests.models import TestModel, QuestionModel
from .signals import post_delete_student_baseuser

BaseUser = get_user_model()


class StudentModel(models.Model):
    """
    Custom Student Model
    """

    # basic fields
    enroll_number = models.CharField(_('Enrollement Number'), max_length=20)
    age = models.PositiveSmallIntegerField(_('age'))
    
    # relational fields
    student_user = models.OneToOneField(get_user_model(), related_name="student_user", on_delete=models.CASCADE, primary_key=True)
    college = models.ForeignKey(related_name="college_students", to=CollegeModel, on_delete=models.CASCADE)
    course = models.ForeignKey(related_name="course_students", to=CourseModel, on_delete=models.CASCADE)
    skills = models.ManyToManyField(related_name="student_skills", to=SkillModel)
    
    def __str__(self) -> str:
        return self.student_user.username
    
    class Meta:
        verbose_name_plural = "Students"
        verbose_name = "Student"


post_delete.connect(post_delete_student_baseuser, StudentModel)


class StudentTestQuestionsModel(models.Model):
    """
    Model for storing answer for each question of a test by a user
    """

    # basic fields
    seleted_option = models.CharField(_('Selected Option'), max_length=1)

    # Relational Fields
    test = models.ForeignKey(to=TestModel, related_name='student_test', on_delete=models.CASCADE)
    question = models.ForeignKey(to=QuestionModel, related_name='student_question', on_delete=models.CASCADE)
    student = models.ForeignKey(to=StudentModel, related_name='student_student', on_delete=models.CASCADE)

    # required methods
    def __str__(self) -> str:
        return f"{self.student.student_user.username}  {self.test.test_name} {self.question.question}" 

    class Meta:
        verbose_name_plural = "Students Tests Questions"
        verbose_name = "Student Test Question"

class StudentTestModel(models.Model):
    """
    Model for storing marks of each student for a test
    """

    # basic fields 
    marks = models.PositiveIntegerField(_('Marks'), default=0)

    # relational fields
    student = models.ForeignKey(to=StudentModel, related_name='test_studnets', on_delete=models.CASCADE)
    test = models.ForeignKey(to=TestModel, related_name='student_tests', on_delete=models.CASCADE)

    # required methods
    def __str__(self) -> str:
        return f"{self.student.student_user.username}  {self.test.test_name}" 

    class Meta:
        verbose_name_plural = "Students Tests"
        verbose_name = "Student Test"