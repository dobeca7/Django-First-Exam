from django.shortcuts import render


def home(request):
    return render(request, "common/home.html")


def custom_404(request, exception):
    return render(request, "common/404.html", status=404)
