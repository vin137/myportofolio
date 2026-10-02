from django.forms import ModelForm, Select, TextInput, Textarea, DateInput, URLInput 
from main.models import Award, Experience
from django.utils.html import strip_tags

class AwardForm(ModelForm):
    class Meta:
        model = Award
        fields = [
            "title",
            "description",
            "date_given"
        ]

        labels = {
            "title": "Nama Award",
            "description": "Deskripsi Award",
            "date_given" : "Tanggal Award",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Contoh: Juara 1 Hackathon",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pencapaian atau deskripsi award ini",
                    "rows": 3,
                }
            ),
            "date_given": DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama award tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Nama Experience",
            "description": "Deskripsi Experience",
            "category" : "Kategori Experience",
            "thumbnail" : "Thumbnail",
            "started_at" : "Tanggal Mulai",
            "ended_at" : "Tanggal Selesai",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Contoh: Teaching Assistant for Math Discrete 1",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Jelaskan pengalamanmu disini",
                    "rows": 3,
                }
            ),
            "category": Select(
                attrs={"class": "form-control"}
            ),
            "thumbnail" : URLInput(
                attrs={
                    "placeholder": "https://example.com",
                }
            ),
            "started_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama experience tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()