from django.core.exceptions import ValidationError

def validate_file_size(value): 
    """
    apply size check on csv file upload
    """
    limit = 1024
    if value.size > limit:
        raise ValidationError(f'File too large. Size should not exceed {limit} Bit.')