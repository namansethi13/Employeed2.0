from django.contrib.auth import get_user_model
from django.template.loader import render_to_string 
from colleges.models import CourseModel
from students.models import StudentModel
from notify.models import NotificationModel
from utils.query_debugger import query_debugger
from tests.models import TestModel
from .models import CorporateModel, JobModel
from .choices import JobStatusType
from .utils import send_test_details
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def handle_job_post(pk, domain, user_id):
    """
    Send Email notification to all the Eligible Students of Eligible Courses
    """
    job_obj = JobModel.objects.get(id=pk)

    job_obj.post_it = JobStatusType.UPDATING
    job_obj.save()
    logger.info("Status changed to UPDATING")

    courses = job_obj.eligible_courses.all()
    students = [student.student_user for student in StudentModel.objects.filter(course__in = courses).select_related('student_user')] 
    test_obj = TestModel.objects.get(job_test = job_obj)
    logger.info(f"student[0] = {students[0].username}")
    logger.info("Job post: Sending emails ..")
    send_test_details(students, domain, job_obj.id)


    # Sending notification with registration link to all eligible and active students
    registration_link = render_to_string('corporates/test_registration_link.html',{
        'domain' : domain,
        'job_id' : job_obj.id,
    })
    body = "New Job Post Based on Your Skills and Preference, check this link for registration" + registration_link
    Notifications = []
    for student in students:
        if student.is_active:
            Notifications.append(NotificationModel(user=student, heading="New Job", body=body, is_seen=False))

    try:
        NotificationModel.objects.bulk_create(Notifications)
        logger.debug("Notification Send Successsfully to all active Students")
    except:
        logger.debug("Notification Send Successsfully to all active Students")

    # Save Notification to the Corporate about Successfully notifiyign all the Students 
    user_obj = get_user_model().objects.get(id=user_id)
    heading = f"Notification send to the Eligible Students"
    body = "We have Notified all the Eligibel Course Students about this through their registed email."
    NotificationModel.objects.create(user=user_obj, heading=heading, body=body, is_seen=False)

    job_obj.post_it = JobStatusType.POSTED
    job_obj.save()
    logger.info("Status changed to POSTED")