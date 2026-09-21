import json
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from main.models import Experience
from main.models import Award
from main.forms import AwardForm, ExperienceForm

def get_awards_json(request):
    title_query = request.GET.get("title", "").strip()
    awards = Award.objects.all()

    if title_query:
        awards = awards.filter(title__icontains=title_query)

    awards_json = serializers.serialize("json", awards)
    return HttpResponse(awards_json, content_type="application/json")


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

def create_experience(request):
    form = ExperienceForm(request.POST or None)
    if(request.method == "POST" and form.is_valid()):
        form.save()
        messages.success(request, "Experience baru berhasil disimpan")
        return redirect("main:show_experience")
    context = {
        "name": "Vincent",
        "form": form,
    }
    return render(request, "experience_form.html", context)    

def delete_experience(request,experience_id):
    experience = get_object_or_404(Experience,pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request,"Experience berhasil dihapus")
    return redirect("main:show_experience")

def edit_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Vincent",
        "form": form,
        "experience": experience
    }
    return render(request, "experience_form.html", context)

def show_award(request):

    json_response = get_awards_json(request)
    
    json_data = json_response.content.decode('utf-8')
    
    parsed_data = serializers.deserialize("json", json_data)
    
    awards = [instance.object for instance in parsed_data]
    
    context = {
        "name": "Vincent",
        "awards": awards,
    }
    return render(request, "award.html", context)


def create_award(request):
    form = AwardForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Award baru berhasil ditambahkan!")
        return redirect("main:show_award")

    context = {
        "name": "Vincent",
        "form": form,
    }
    return render(request, "award_form.html", context)

def delete_award(request, award_id):
    award = get_object_or_404(Award, pk=award_id)

    if request.method == "POST":
        award.delete()
        messages.success(request, "Award berhasil dihapus!")
        return redirect("main:show_award")

    return redirect("main:show_award")

def edit_award(request,award_id):
    award = get_object_or_404(Award,pk = award_id)
    form = AwardForm(request.POST or None,instance=award)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("main:show_award")

    context = {
        "name": "Vincent",
        "form": form,
        "award" : award
    }
    return render(request, "award_form.html", context)