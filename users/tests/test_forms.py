from django.test import TestCase
from ..models import CustomUser, Transfer
from ..forms import TransferForm
from django.urls import reverse


class TransferFormTest(TestCase):

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

    def test_post(self):
        form = TransferForm(
            {
                'sender': self.sender,
                'amount': self.transfer.amount,
                'receiver': self.receiver.inn
            }
        )
        self.assertTrue(form.is_valid())

    def test_balance(self):
        url = reverse("users:transfer-list")
        response = self.client.get(url)
        if int(self.sender.billing) - int(self.transfer.amount) >= int(0):
            self.assertTrue(response.status_code, 200)

    def test_inn(self):
        url = reverse("users:transfer-list")
        # receiver inn
        response = self.client.put(url, self.receiver.inn)
        self.assertTrue(response.status_code, 200)
        # self inn
        response = self.client.put(url, self.sender.inn)
        self.assertTrue(response.status_code, 400)
