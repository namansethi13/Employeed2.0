from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import DetailView
from django.contrib import messages
from tests.models import TestModel
from corporates.models import SkillModel, JobModel
from students.models import StudentModel, StudentTestModel
from notify.models import NotificationModel
from utils.query_debugger import query_debugger
import logging

logger = logging.getLogger(__name__)

@query_debugger
def student_dashboard(request):
    student_obj = StudentModel.objects.filter(student_user = request.user)[0]
    registered_tests = StudentTestModel.objects.filter(student = student_obj, marks = 0).select_related()
    tests = []
    for registered_test in registered_tests:
        tests.append(registered_test.test)
    print("tests", tests)
    return render(request, 'students/student_dashbord.html', {'tests': tests})

class JobRegistrationDetialView(DetailView):
    template_name = 'students/student_job_details.html'
    model = JobModel

    def get_context_data(self, **kwargs):
        context = super(JobRegistrationDetialView, self).get_context_data(**kwargs)
        job_obj = JobModel.objects.filter(id=kwargs['object'].id)[0]
        context['skills'] = job_obj.skills.all()
        context['courses'] = job_obj.eligible_courses.all()
        context['test_obj'] = TestModel.objects.filter(job_test=job_obj)[0]
        return context

@query_debugger
def test_register(request, pk):
    try:
        #  checking wheater this student is Eligible for it
        test_obj = TestModel.objects.filter(id=pk).select_related('job_test')[0]
        # job_obj = test_obj.job_test
        print(request.user)
        student_obj = StudentModel.objects.filter(student_user = request.user.id)[0]
        # logger.info(f'job = {job_obj}')
        # logger.info(f'student = {student_obj}')

        if StudentTestModel.objects.filter(student = student_obj, test = test_obj).exists():
            messages.error(request,"You have been already Registered")
            logger.error("You have been already Registered")
        else:
            StudentTestModel.objects.create(student = student_obj, test = test_obj, marks = 0)
            messages.info(request,"Registered Successfully")
            logger.info("Registered Successfully")
    except:
        logger.info(f"Error while registering for test")

    return redirect(reverse('student_dashboard'))