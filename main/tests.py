import uuid
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.models import Award
from main.models import Experience
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class SectionApiTestsMixin:

    model = None
    prefix = None            # "award" atau "experience"
    valid_payload = None     # payload valid lengkap (untuk POST/PUT)
    patch_payload = {"title": "Judul Baru"}

    def setUp(self):
        editor_group = Group.objects.create(name="Editor")
        self.regular = User.objects.create_user(
            "regular", "regular@example.com", "pass12345"
        )
        self.editor = User.objects.create_user(
            "editor", "editor@example.com", "pass12345"
        )
        self.editor.groups.add(editor_group)
        self.owner = User.objects.create_superuser(
            "owner", "owner@example.com", "pass12345"
        )
        self.obj = self.model.objects.create(
            title="Judul Lama", description="Deskripsi lama"
        )
        self.list_url = reverse(f"api:{self.prefix}-list")
        self.detail_url = reverse(f"api:{self.prefix}-detail", args=[self.obj.pk])
        self.star_url = reverse(f"api:{self.prefix}-star", args=[self.obj.pk])

    def as_user(self, user=None):
        client = APIClient()
        if user is not None:
            client.force_authenticate(user=user)
        return client

    def test_visitor_can_read_list_and_detail(self):
        client = self.as_user()
        self.assertEqual(client.get(self.list_url).status_code, status.HTTP_200_OK)
        response = client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Judul Lama")
        self.assertFalse(response.data["is_starred"])

    def test_detail_not_found_returns_404(self):
        url = reverse(f"api:{self.prefix}-detail", args=[uuid.uuid4()])
        self.assertEqual(self.as_user().get(url).status_code, status.HTTP_404_NOT_FOUND)

    def _assert_write_denied(self, client):
        count = self.model.objects.count()

        response = client.post(self.list_url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.model.objects.count(), count)

        response = client.patch(self.detail_url, self.patch_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = client.put(self.detail_url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.title, "Judul Lama")

        response = client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(self.model.objects.filter(pk=self.obj.pk).exists())

    def test_visitor_cannot_write(self):
        self._assert_write_denied(self.as_user())

    def test_regular_user_cannot_write(self):
        self._assert_write_denied(self.as_user(self.regular))

    def test_editor_can_patch_and_put(self):
        client = self.as_user(self.editor)
        response = client.patch(self.detail_url, self.patch_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.title, "Judul Baru")

        payload = dict(self.valid_payload, title="Judul Put")
        response = client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.title, "Judul Put")

    def test_editor_cannot_create_or_delete(self):
        client = self.as_user(self.editor)
        count = self.model.objects.count()

        response = client.post(self.list_url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.model.objects.count(), count)

        response = client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(self.model.objects.filter(pk=self.obj.pk).exists())

    # ------------------------------------------------------------- owner
    def test_owner_can_create(self):
        count = self.model.objects.count()
        response = self.as_user(self.owner).post(
            self.list_url, self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.model.objects.count(), count + 1)
        self.assertTrue(
            self.model.objects.filter(title=self.valid_payload["title"]).exists()
        )

    def test_owner_can_patch(self):
        response = self.as_user(self.owner).patch(
            self.detail_url, self.patch_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.title, "Judul Baru")

    def test_owner_can_delete(self):
        response = self.as_user(self.owner).delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.model.objects.filter(pk=self.obj.pk).exists())

    def test_invalid_input_returns_400(self):
        client = self.as_user(self.owner)
        count = self.model.objects.count()
        payload = dict(self.valid_payload, title="<b></b>")
        response = client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
        self.assertEqual(self.model.objects.count(), count)

    def test_missing_title_returns_400(self):
        payload = {k: v for k, v in self.valid_payload.items() if k != "title"}
        response = self.as_user(self.owner).post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_html_tags_are_stripped(self):
        payload = dict(
            self.valid_payload,
            title="<script>alert(1)</script>Judul Bersih",
            description="<b>Tebal</b> biasa",
        )
        response = self.as_user(self.owner).post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        saved = self.model.objects.get(pk=response.data["id"])
        self.assertNotIn("<", saved.title)
        self.assertNotIn(">", saved.title)
        self.assertEqual(saved.description, "Tebal biasa")

    def test_invalid_patch_does_not_change_db(self):
        response = self.as_user(self.editor).patch(
            self.detail_url, {"title": "<i></i>"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.title, "Judul Lama")

    def test_search_by_title_query_param(self):
        self.model.objects.create(title="Hackathon Nasional", description="x")
        response = self.as_user().get(self.list_url, {"title": "hackathon"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data]
        self.assertEqual(titles, ["Hackathon Nasional"])

    def test_visitor_cannot_star(self):
        response = self.as_user().post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.obj.starred_by.count(), 0)

    def test_star_toggle(self):
        client = self.as_user(self.regular)
        response = client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(response.data["is_starred"])
        self.assertTrue(self.obj.starred_by.filter(pk=self.regular.pk).exists())

        response = client.post(self.star_url)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(self.obj.starred_by.count(), 0)

    def test_star_uses_request_user_not_body(self):
        client = self.as_user(self.regular)
        client.post(self.star_url, {"user": self.owner.pk}, format="json")
        self.assertTrue(self.obj.starred_by.filter(pk=self.regular.pk).exists())
        self.assertFalse(self.obj.starred_by.filter(pk=self.owner.pk).exists())

    def test_star_on_missing_object_returns_404(self):
        url = reverse(f"api:{self.prefix}-star", args=[uuid.uuid4()])
        response = self.as_user(self.regular).post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sensitive_user_data_not_exposed(self):
        self.obj.starred_by.add(self.regular)
        response = self.as_user().get(self.detail_url)
        body = response.content.decode()
        self.assertNotIn("regular@example.com", body)
        self.assertNotIn("password", body)

    def test_write_without_csrf_token_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="pass12345"))
        count = self.model.objects.count()

        response = client.post(self.list_url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.model.objects.count(), count)

        response = client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(self.model.objects.filter(pk=self.obj.pk).exists())

        response = client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.obj.starred_by.count(), 0)


class AwardApiTests(SectionApiTestsMixin, APITestCase):
    model = Award
    prefix = "award"
    valid_payload = {
        "title": "Juara 1 Hackathon",
        "description": "Lomba tingkat nasional",
        "date_given": "2026-05-01",
    }


class ExperienceApiTests(SectionApiTestsMixin, APITestCase):
    model = Experience
    prefix = "experience"
    valid_payload = {
        "title": "Teaching Assistant",
        "description": "Asisten dosen Matdis 1",
        "category": "part-time",
        "thumbnail": "https://example.com/ta.png",
        "started_at": "2026-01-01T00:00:00Z",
        "ended_at": None,
    }

class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse('main:get_experiences_json'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.experience.title)

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        response = self.client.get(reverse('main:get_experiences_json'))
        
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Sedang berlangsung")


    
    def test_award_page_url_and_template(self):
        response = self.client.get(reverse('main:show_award'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'award.html')

    def test_award_page_empty_condition(self):
        response = self.client.get(reverse('main:show_award'))
        self.assertContains(response, "Belum ada award yang ditambahkan.")


    def test_edit_award_functionality(self):
        user = User.objects.create_superuser(username='admintes', password='password123')
        self.client.login(username='admintes', password='password123')

        award = Award.objects.create(
            title="Award Lama", 
            description="Deskripsi Lama"
        )
        response = self.client.post(
            reverse('main:edit_award', args=[award.id]), 
            {'title': 'Award Baru', 'description': 'Deskripsi Baru', 'date_given': '2026-10-02'}
        )
        self.assertRedirects(response, reverse('main:show_award'))
        
        award.refresh_from_db()
        self.assertEqual(award.title, "Award Baru")


    def test_delete_award_functionality(self):
        user = User.objects.create_superuser(username='admintesdelete', password='password123')
        
        self.client.login(username='admintesdelete', password='password123')

        award = Award.objects.create(
            title="Award Mau Dihapus", 
            description="Deskripsi"
        )
        response = self.client.post(reverse('main:delete_award', args=[award.id]))
        self.assertRedirects(response, reverse('main:show_award'))
        self.assertFalse(Award.objects.filter(id=award.id).exists())

    def test_award_page_with_data(self):
        Award.objects.create(
            title="Juara 1 Hackathon UI 2026", 
            description="Memenangkan kompetisi coding tingkat nasional."
        )
        response = self.client.get(reverse('main:get_awards_json')) 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Juara 1 Hackathon UI 2026")
        self.assertContains(response, "Memenangkan kompetisi coding tingkat nasional.")

    def test_experience_page_with_data(self):
        Experience.objects.create(
            title="Teaching Assistant", 
            description="Mengajar kelas matematika diskrit."
        )
        response = self.client.get(reverse('main:get_experiences_json'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teaching Assistant")
