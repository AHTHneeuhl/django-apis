from rest_framework.exceptions import ValidationError


def validate_file_size(file):
    """
    Ensure resume file size does not exceed 1MB.
    """
    max_size = 2 * 1024  # 1MB

    if file.size > max_size:
        raise ValidationError("Resume file size must not exceed 1MB.")