from django.test import Client, TestCase
from user.models import User
from user.factories import UserFactory


class UserFactoryTests(TestCase):
    def setUp(self):
        """
        läuft VOR jeder Testmethode
        """
        self.client = Client()
        self.user = UserFactory(username="testuser")

    def test_user_is_created(self):
        """Prüfe, User existiert"""
        userexists = User.objects.filter(username="testuser").exists()
        self.assertTrue(userexists)
