import re
from django.shortcuts import redirect

class CleanURLMiddleware:
    """
    Membersihkan karakter tidak valid dari URL secara global.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Hanya izinkan huruf, angka, slash, dash, underscore, dan titik
        self.allowed_pattern = re.compile(r'[^a-zA-Z0-9/_\-.]')

    def __call__(self, request):
        original_path = request.path_info
        cleaned_path = re.sub(self.allowed_pattern, '', original_path)

        if cleaned_path != original_path:
            return redirect(cleaned_path)

        return self.get_response(request)
