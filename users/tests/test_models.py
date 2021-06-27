from django.test import TestCase
from ..models import CustomUser, Transfer


class CustomUserTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='usertest',
            password='userpass',
            inn='555555555555',
            billing='1000'
        )

    def test_create(self):
        self.assertEqual(self.user.username, 'usertest')
        self.assertEqual(self.user.password, 'userpass')
        self.assertEqual(self.user.inn, '555555555555')
        self.assertEqual(self.user.billing, '1000')


class TransferTest(TestCase):

    def setUp(self):

        self.user_1 = CustomUser.objects.create(
            username='usertest',
            password='userpass',
            inn='555555555555',
            billing='1000'
        )

        self.user_2 = CustomUser.objects.create(
            username='usertest2',
            password='userpass',
            inn='444444444444',
            billing='1000'
        )

        self.transfer = Transfer.objects.create(
            sender=self.user_1,
            amount=100.00
        )
        self.transfer.receiver.add(self.user_2)

    def test_create(self):
        transfer = Transfer.objects.all().first()
        self.assertEqual(transfer.sender, self.user_1)
        self.assertEqual(transfer.receiver.all().first(), self.user_2)
        self.assertEqual(transfer.amount, self.transfer.amount)
