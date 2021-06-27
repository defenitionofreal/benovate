from django.test import TestCase
from ..models import CustomUser, Transfer
from django.urls import reverse


class CustomUserTest(TestCase):

    def setUp(self):
        self.user_1 = CustomUser.objects.create(
            username='user',
            password='pass',
            inn='555555555555',
            billing='1000'
        )
        self.user_2 = CustomUser.objects.create(
            username='usertest',
            password='pass',
            inn='444444444444',
            billing='1000'
        )

    def test_users_page(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('users_list.html')

    def test_list(self):
        url = reverse("users:user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("users_list.html")
        self.assertContains(response, self.user_1)
        self.assertContains(response, self.user_2)

    def test_detail(self):
        url = reverse("users:user-detail", args=(self.user_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('user_detail.html')
        self.assertContains(response, self.user_1.username)
        self.assertContains(response, self.user_1.inn)
        self.assertContains(response, self.user_1.billing)


class TranferTest(TestCase):

    def setUp(self):
        self.sender = CustomUser.objects.create(
            username='usertest',
            inn='555555555555',
            billing='1000'
        )
        self.receiver = CustomUser.objects.create(
            username='usertest2',
            inn='444444444444',
            billing='1000'
        )
        self.transfer = Transfer.objects.create(
            sender=self.sender,
            amount=100
        )
        self.transfer.receiver.add(self.receiver)

    def test_transfer_page(self):
        response = self.client.get('/transfer/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('transfer_form.html')

    def test_get_list(self):
        url = reverse("users:transfer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("transfer_form.html")
        self.assertContains(response, self.sender.id)
        self.assertContains(response, self.transfer.receiver)
        self.assertContains(response, self.transfer.amount)
