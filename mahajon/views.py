from django.shortcuts import redirect


def index(request):
    return redirect('https://mahajon.com', permanent=True)