from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from colleges.models import CourseModel
from .choices import JobStatusType

BaseUser = get_user_model()


class CorporateModel(BaseUser):
    """
    Custom Corporate Model
    """
    company_name = models.CharField(_('Company Name'), max_length=100, blank=True, null=True, unique=True)
    address = models.CharField(_('Address'), max_length=255, blank=True, null=True)
    website = models.URLField(_('Website'), max_length=255, blank=True, null=True)
    description = models.CharField(_('Description'), max_length=1000, blank=True, null=True)
    
    def __str__(self) -> str:
        return  self.username

    class Meta:
        verbose_name_plural = 'corporates'


class SkillModel(models.Model):
    """
    Skill Model
    """
    skill_name = models.CharField(_('Skill Name'), max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "skills"
        verbose_name = "skill"

    def __str__(self) -> str:
        return self.skill_name

    def save(self, *args, **kwargs):
        self.skill_name = str(self.skill_name).lower()
        return super(SkillModel, self).save(*args, **kwargs)


class JobModel(models.Model):
    """
    Job model, which a Corporate can post
    """

    # basic fields
    job_name = models.CharField(_('Job Name'), max_length=255)
    job_description = models.TextField(_('Job Description'))
    eligibility = models.TextField(_('Eligibilty'), default='Open for all')
    post_it = models.CharField(_('Post It'), max_length=10, default=JobStatusType.PRIVATE, choices = JobStatusType.choices)
    
    # relational fields
    skills = models.ManyToManyField(SkillModel, related_name='job_skills')
    eligible_courses = models.ManyToManyField(CourseModel, related_name='job_courses')
    owner = models.ForeignKey(CorporateModel, related_name='jobs', on_delete=models.CASCADE)

    # required methods
    def __str__(self) -> str:
        return self.job_name

    class Meta:
        verbose_name_plural = "jobs"
        verbose_name = "job"