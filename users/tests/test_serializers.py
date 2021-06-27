from django.test import TestCase
from ..models import CustomUser
from ..serializers import CustomUserSerializer, TransferSerializer


class CustomUserSerializerTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='usertest',
            first_name='test',
            last_name='test',
            inn='555555555555',
            billing='1000'
        )

    def test_data(self):
        data = CustomUserSerializer(self.user).data
        expected_data = {'id': 1,
                         'username': 'usertest',
                         'first_name': 'test',
                         'last_name': 'test',
                         'inn': '555555555555',
                         'billing': '1000.00'}

        self.assertEqual(expected_data, data)


class TransferSerializerTest(TestCase):

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

    def test_data(self):
        data = TransferSerializer({
            'sender': self.sender,
            'receiver': self.receiver.inn,
            'amount': 100
        }).data
        expected_data = {
            'sender': self.sender.id,
            'receiver': self.receiver.inn,
            'amount': str("100.00")
        }
        self.assertEqual(expected_data, data)
