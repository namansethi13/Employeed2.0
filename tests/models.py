from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from corporates.models import SkillModel, CorporateModel, JobModel


class TestModel(models.Model):
    """
    TestModel which will belong to only 1 user
    """
    # basic fields
    test_name = models.CharField(_('Test Name'), max_length=255)
    description = models.TextField(_('Description'))
    total_questions = models.PositiveIntegerField(_('Total Questions'),
        validators=[ 
            MinValueValidator(5), 
            MaxValueValidator(100)
        ],
        default=10
    )
    pass_percentage = models.PositiveIntegerField(_('Pass Percentage'),
        validators=[ 
            MinValueValidator(0), 
            MaxValueValidator(100)
        ]
    )
    
    # operational fields
    start_date = models.DateField(_('Start Date'), auto_now=False, auto_now_add=False)
    end_date = models.DateField(_('End Date'), auto_now=False, auto_now_add=False)
    duration = models.PositiveIntegerField(_('Duration'))
    
    # Relational fields
    job_test = models.OneToOneField(to=JobModel, on_delete=models.CASCADE, related_name='job_test')
    owner = models.ForeignKey(to=CorporateModel, on_delete=models.CASCADE)

    # extra fields
    created_at = models.DateTimeField(_("Created Datetime"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated Datetime"), auto_now=True)

    class Meta:
        verbose_name_plural = "tests"
        verbose_name = "test"
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.test_name

    def clean(self) -> None:
        if self.start_date >= self.end_date:
            raise ValidationError("{'start_date' : Start Date should be before the End Date}")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    


class QuestionModel(models.Model):
    """
    Question Model, stores MCQ questions
    """
    ANSWER_CHOISE = (
        ('A', 'A'), 
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )


    # basic fields
    question = models.TextField(_('Question'), max_length=1000)
    A = models.CharField(_('A'), max_length=255)
    B = models.CharField(_('B'), max_length=255)
    C = models.CharField(_('C'), max_length=255)
    D = models.CharField(_('D'), max_length=255)
    answer = models.CharField(_('Answer'), max_length=1, choices=ANSWER_CHOISE)

    # operational fields
    is_public = models.BooleanField(_('Is Public'), default=False)
    
    # relational fields
    test = models.ManyToManyField(to=TestModel, related_name='tests_questions')
    skill = models.ForeignKey(to=SkillModel, on_delete=models.CASCADE)
    owner = models.ForeignKey(to=CorporateModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "questions"
        verbose_name = "question"
        ordering = ['id']

    def __str__(self) -> str:
        return self.question