
class StudentEmailAlreadyInDatabaseException(Exception):
    msg = "Students with provides email are already is in database"

class StudentEmailSendException(Exception):
    msg = "We are facing issue with sending emails to the students"

class CollegeEmailSendException(Exception):
    msg = "We faced issue to send email to college about student registrations"