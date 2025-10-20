from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.urls import resolve, Resolver404

class NotFoundMiddleware:
    """
    Middleware global untuk menangani URL yang tidak ditemukan,
    dan otomatis menampilkan halaman 404.html custom.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Coba resolve URL
        try:
            resolve(request.path_info)
        except Resolver404:
            # Jika tidak ditemukan, tampilkan 404.html
            return HttpResponseNotFound(render(request, '404.html'))

        # Jika URL valid → lanjut proses normal
        response = self.get_response(request)
        return response
