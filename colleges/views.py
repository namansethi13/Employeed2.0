from django.http import HttpResponse
from django.views import View
from django.core.exceptions import ValidationError
from colleges.exceptions import (
    CollegeEmailSendException,
    StudentEmailAlreadyInDatabaseException,
    StudentEmailSendException
)
from students.models import StudentModel
from .models import CollegeModel, CollegesCourses, CourseModel
from .forms import AddCourceForm, UploadCsvForm
from .tasks import handle_uploaded_file
from .choices import AddingStudentStatusType
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from utils.query_debugger import query_debugger
from django.contrib.sites.shortcuts import get_current_site 
import logging
import csv
import os

logger = logging.getLogger(__name__)


class CollegeDashboardView(View):
    """
    College Dashboard : 
    - Add new Courses
    - Upload student in the course
    - Update student of a course
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.course_form = AddCourceForm()
        self.upload_csv_form = UploadCsvForm()

    def get(self, request):
        try:
            # getting list of courses the current college offers
            print("usernaem = ", request.user.username)
            college_obj = CollegeModel.objects.filter(username=request.user.username)[0]
            college_course_objs = CollegesCourses.objects.filter(college = college_obj)
            courses = [(obj.course, obj.status ) for obj in college_course_objs]

            # storing it in the Sessions
            request.session['courses'] = [obj[0].abbrevation for obj in courses]

            request.session.modified = True

            print("Session = ", request.session['courses'])

            context = {
                'courses' : courses,
                'course_form': self.course_form,
                'uploac_csv_form' : self.upload_csv_form,
            }
        except:
            context = {}
            logger.exception("Get request Failed")
        return render(request, 'colleges/college_dashboard.html', context = context)

    def post(self, request):
        try:
            # current college object
            college_obj = CollegeModel.objects.filter(username=request.user.username)[0]

            form = AddCourceForm(request.POST, None)

            if form.is_valid():
                selected_courses = form.cleaned_data.get('course_options')
            else:
                logger.warning("Form is Invalid")
                messages.warning(request, "Form is Invalid")
                return redirect(reverse_lazy('college_dashboard'))

            # selecting only new courses ticked
            if 'courses' in request.session:
                selected_courses = list(set(selected_courses) - set(request.session['courses']))

            invalid_courses = []
            college_course_objs = []
            for selected_course in selected_courses:
                if CourseModel.objects.filter(abbrevation__exact = selected_course).exists():
                    course_obj = CourseModel.objects.get(abbrevation=selected_course)
                    college_course_objs.append(CollegesCourses(college = college_obj, course = course_obj))
                else:
                    invalid_courses.append(selected_course)

            if len(invalid_courses):
                logger.warning(f"These Course are not in database : {invalid_courses}")
                messages.warning(request, f"These Course are not in database : {invalid_courses}")
            else:
                CollegesCourses.objects.bulk_create(college_course_objs)
                logger.info("Course added successfully")
                messages.success(request, "Course added successfully")
        except:
            logger.exception("Error in Handling Post request, Add course")
            messages.error(request, "Error in Handling Post request, Add course")

        # redirecting to dashboard with get request
        return redirect(reverse_lazy('college_dashboard'))

    
def delete_course_from_college(request, pk):
    if request.method == 'GET':
        try:
            # getting course_obj, college_obj, and College_Course_obj for deleting it
            course_obj = CourseModel.objects.filter(pk=pk)[0]
            college_obj = CollegeModel.objects.filter(username=request.user.username)[0]

            with transaction.atomic():
                # delete only when status is not UPDATING
                college_course_obj = CollegesCourses.objects.filter(
                    college = college_obj, course = course_obj).exclude(
                    status=AddingStudentStatusType.UPDATING)[0]

                if college_course_obj.status == 'UPDATED':
                    student_delete = StudentModel.objects.filter(college=college_obj, course = course_obj).delete()
                
                college_course_obj.delete()

            logger.info(f"{course_obj.abbrevation} Course Deleted  Successfully")
            messages.success(request, f"{course_obj.abbrevation} Course Deleted  Successfully")
        except:
            logger.exception(f"Error while deleteing the Course {course_obj.abbrevation}")
            messages.error(request, f"Error while deleteing the Course {course_obj.abbrevation}")
        return redirect(reverse_lazy('college_dashboard'))

def download_sample_csv(request):
    """
    Download Sample Csv file for adding student data of a course
    """
    if request.method == 'GET':
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="student_data_sample.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['Email', 'Enroll number', 'Age'])
        writer.writerow(['dummyemail@domain.com', '001345602022', 21])

        return response
    else:
        logger.exception("Request for downloading should be GET")
        messages.error(request, "Request for downloading should be GET")
        return redirect(reverse_lazy('college_dashboard'))

def upload_student_data(request):
    """
    Registed Students of a praticular course provided with the csv data
    """
    if request.method == 'POST':
        try:
            form = UploadCsvForm(request.POST, request.FILES)
            if form.is_valid():
                # getting required variables ready
                course_id = form.cleaned_data.get('course_id')
                course_obj = CourseModel.objects.filter(id = course_id)[0]
                college_obj = CollegeModel.objects.filter(username=request.user.username)[0]
                college_course_obj = CollegesCourses.objects.filter(college = college_obj, course = course_obj)[0]
                college_course_obj.status = AddingStudentStatusType.UPDATING
                college_course_obj.save()

                # Saving file to disk
                file_name = f'{college_obj.username}_{course_obj.abbrevation}.csv'
                file = form.cleaned_data.get('csv_file')
                fs = FileSystemStorage()
                file_name = fs.save(file_name, file) 

                domain = get_current_site(request).domain
                handle_uploaded_file.delay(file_name, request.user.id, domain, college_obj.id, course_obj.id, college_course_obj.id)

                logger.info("Uploaded file is valid")
                messages.info(request, "Uploaded file is valid")
            else:
                logger.error("Uploaded file is not valid or max size limit exceded")
                messages.error(request, "Uploaded file is not valid or max size limit exceded")
        except StudentEmailAlreadyInDatabaseException as e:
            logger.exception(f"StudentEmailAlreadyInDatabaseException : {e.msg}")
            messages.error(request, f"{e.msg}")
        except StudentEmailSendException as e:
            logger.exception("StudentEmailSendException : {e.msg}")
            messages.error(request, "StudentEmailSendException :{e.msg}")
        except CollegeEmailSendException as e:
            logger.exception("CollegeEmailSendException : {e.msg}")
            messages.error(request, "CollegeEmailSendException :{e.msg}")
        except ValidationError as e:
            logger.exception("ValidationError : {e.msg}")
            messages.error(request, "ValidationError :{e.msg}")
        
        return redirect(reverse_lazy('college_dashboard'))

def retrieve_students(request, pk):
    """
    pk: id of couse object
    returns all students of a coures and college
    """
    try:
        course_obj = CourseModel.objects.filter(id=pk)[0]
        college_obj = CollegeModel.objects.filter(username=request.user.username)[0]
        students = StudentModel.objects.select_related("student_user").filter(college=college_obj, course=course_obj)
        return render(request, 'colleges/students_list.html', {'students' : students, 'course' : course_obj})
    except:
        logger.exception("Error: while retrievel students list")
        messages.error(request, "Error: while retrievel students list")
    
    return redirect(reverse_lazy('college_dashboard'))
    