import json
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from main.models import Experience
from main.models import Award
from main.forms import AwardForm, ExperienceForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST


def get_awards_json(request):
    title_query = request.GET.get("title", "").strip()
    awards = Award.objects.prefetch_related('starred_by').all()

    if title_query:
        awards = awards.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for award in awards:
        starred_users = award.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(award.id),
            "fields": {
                "title": award.title,
                "description": award.description,
                "date_given" : award.date_given,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Vincent",
        "npm": "2506618540",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS student at Universitas Indonesia."""
            "Majoring in Computer Science."
            "Interested in Competitive Programming, Artificial Intelligence, and Robotics."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    is_editor = request.user.is_authenticated and request.user.groups.filter(name='Editor').exists()
    context = {
        "name": "Vincent",
        "experience_list": Experience.objects.all(),
        "is_editor" : is_editor,
    }
    return render(request, "experience.html", context)

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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

@login_required(login_url="/login/") 
def delete_experience(request,experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience,pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request,"Experience berhasil dihapus")
    return redirect("main:show_experience")

@login_required(login_url="/login/")
def edit_experience(request, experience_id):
    is_editor = request.user.groups.filter(name='Editor').exists()
    if not (request.user.is_superuser or is_editor):
        raise PermissionDenied

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

@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    project = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_experience")

def show_award(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Vincent",
        "title_query": title_query,
        "form":AwardForm(),
    }
    return render(request, "award.html", context)

@login_required(login_url="/login/") 
def create_award(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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

@login_required(login_url="/login/") 
def delete_award(request, award_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    award = get_object_or_404(Award, pk=award_id)

    if request.method == "POST":
        award.delete()
        messages.success(request, "Award berhasil dihapus!")
        return redirect("main:show_award")

    return redirect("main:show_award")

@login_required(login_url="/login/") 
def edit_award(request,award_id):
    is_editor = request.user.groups.filter(name='Editor').exists()
    if not (request.user.is_superuser or is_editor):
        raise PermissionDenied

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

@login_required(login_url="/login/")
def toggle_star_award(request, award_id):
    project = get_object_or_404(Award, pk=award_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_award")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@require_POST
def create_award_ajax(request):
    # Validasi otorisasi server-side
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan award."},
            status=403,
        )

    # Memanfaatkan kembali AwardForm dari Tugas 3 & 4
    form = AwardForm(request.POST)
    if form.is_valid():
        award = form.save()
        return JsonResponse(
            {"message": "Award berhasil ditambahkan.", "pk": str(award.id)},
            status=201,
        )

    # Mengembalikan struktur error jika tidak valid
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)