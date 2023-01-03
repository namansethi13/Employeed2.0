from .models import  CourseModel, CollegesCourses, CollegeModel
from students.models import StudentModel
from accounts.choices import RoleType
from .choices import AddingStudentStatusType
from django.contrib.auth import get_user_model
from .exceptions import StudentEmailAlreadyInDatabaseException
from .utils import send_credentials_email, notify_through_email
from notify.models import NotificationModel
from celery import shared_task
from django.conf import settings
import random
import logging
import csv
import os
import uuid
logger = logging.getLogger(__name__)

BASEUSER = get_user_model()

@shared_task
def handle_uploaded_file(file_name, user_id, domain, college_id, course_id, college_course_id):
    user_obj = get_user_model().objects.filter(id = user_id)[0]
    college_obj = CollegeModel.objects.filter(id = college_id)[0]
    course_obj = CourseModel.objects.filter(id=course_id)[0]
    college_course_obj = CollegesCourses.objects.filter(id= college_course_id)[0]

    # bulk creating BaseUser as Student, and storing them in student_user list
    STUDENT_USERS = []
    ENROLL_NUMBERS = []
    AGES = []
    PASSWORDS = []
    STUDENT_EMAILS = []

    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            email = str(row[0])
            username = email.split('@')[0] + str(random.randint(0,99999))
            password=str(uuid.uuid4())
            STUDENT_USERS.append(
                BASEUSER(username=username, email=email, password=str(uuid.uuid4()), role=RoleType.STUDENT)
            )
            PASSWORDS.append(password)
            ENROLL_NUMBERS.append(str(row[1]))
            AGES.append(int(row[2]))
            STUDENT_EMAILS.append(email)

    os.remove(file_path)

    try:
        STUDENT_USERS = BASEUSER.objects.bulk_create(STUDENT_USERS)
    except:
        already_registered_list = []
        for student_email in STUDENT_EMAILS:
            if BASEUSER.objects.filter(email__exact = student_email).exists():
                already_registered_list.append(student_email)

        heading = f"Some student's email has been already registered pls check them"
        body = f"""These emails are already is in database, please double check them, 
            and provide with a differnt emails
            {already_registered_list}
        """
        NotificationModel.objects.create(user=user_obj, heading=heading, body=body, is_seen=False)
        logger.error(body)

        college_course_obj.status = AddingStudentStatusType.NO_DATA
        college_course_obj.save()

        logger.info(f"already registered = {already_registered_list}", )
        return "Error: notified about duplicate emails in database"

    logger.info("Student BaseUser created Successfully")

    # bulk creating StudentModel instances, using STUDENT_USERS, ENROLL_NUMBERS, AGES 
    STUDENT_OBJS = []

    for i in range(0, len(STUDENT_USERS)):
        STUDENT_OBJS.append(StudentModel(
            student_user=STUDENT_USERS[i],
            enroll_number = ENROLL_NUMBERS[i],
            age = AGES[i],
            college = college_obj,
            course = course_obj,
            )
        )
    
    logger.info("Student OBJS")

    try:
        STUDENT_OBJS = StudentModel.objects.bulk_create(STUDENT_OBJS)
    except:
        logger.info("StudentModel Instances created Successfully")


    send_credentials_email(domain, STUDENT_USERS, PASSWORDS)
    
    notify_through_email(college_obj, course_obj)

    # Save Notification in NotificationModel Table, will send notification atomatically
    heading = f"Saved and Registered Students of {course_obj.abbrevation} Course"
    body = "Students Accounts created Successfully, they can now login to the website throght the credentials provided in their registered emails."
    NotificationModel.objects.create(user=user_obj, heading=heading, body=body, is_seen=False)

    college_course_obj.status = AddingStudentStatusType.UPDATED
    college_course_obj.save()
    logger.info("Status changed to UPDATED")

    return "Sudents got added :>"
