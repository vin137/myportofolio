from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.models import Award
from main.models import Experience


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