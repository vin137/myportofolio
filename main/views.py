from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Vincent",
        "npm": "2506618540",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS student at Universitas Indonesia."""
            "Majoring in Computer Science."
            "Interested in Competitive Programming, Artificial Intelligence, and Robotics."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Vincent",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)