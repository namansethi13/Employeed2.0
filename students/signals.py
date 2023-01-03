# <------------      College/Signals.py        ----------------->#


def post_delete_student_baseuser(sender, instance, *args, **kwargs):
    """
    Delete the Base user Instances of a Student if Student get deleted
    """
    instance.student_user.delete()