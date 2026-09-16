from django.forms import ModelForm, TextInput, Textarea, DateInput 
from main.models import Award

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
