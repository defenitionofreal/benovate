from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status, serializers
from ..models import CustomUser
from ..serializers import CustomUserSerializer
from rest_framework.test import APIRequestFactory
from ..views import UserViewSet


class CustomUserAPITest(APITestCase):

    def setUp(self):
        self.user_1 = CustomUser.objects.create(
            username='user',
            inn='555555555555',
            billing='1000'
        )

        self.user_2 = CustomUser.objects.create(
            username='usertest',
            inn='444444444444',
            billing='1000'
        )

        self.factory = APIRequestFactory()
        self.view = UserViewSet.as_view({'get': 'list',
                                         'post': 'create', })

    def test_get_list(self):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True).data
        request = self.factory.get(reverse("users:customuser-list"))
        response = self.view(request)
        self.assertEqual(response.data, serializer)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one(self):
        serializer = CustomUserSerializer(self.user_1).data
        url = reverse("users:customuser-detail", args=(self.user_1.id,))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer, response.data)

    def test_create(self):
        data = {
            "username": "erik",
            "password": "pass123erik321",
        }
        response = self.client.post(
            reverse("users:customuser-list"), data=data)
        self.assertEqual(CustomUser.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        data = {
            "username": "erik",
            "password": "pass",
        }
        url = reverse("users:customuser-detail", args=(self.user_1.id,))
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse("users:customuser-detail", args=(self.user_1.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TransactionTestCase(APITestCase):

    def setUp(self):
        self.user_1 = CustomUser.objects.create(
            username='user',
            inn='555555555555',
            billing='1000'
        )

        self.user_2 = CustomUser.objects.create(
            username='usertest',
            inn='444444444444',
            billing='500'
        )

        self.user_3 = CustomUser.objects.create(
            username='usertest3',
            inn='222222222222',
            billing='100'
        )

    def test_create(self):
        url = reverse("users:transfer-list")
        data = {
            'sender': self.user_1.id,
            'amount': 1000,
            'receiver': self.user_2.inn
        }
        response = self.client.post(
            url,
            data=data,
        )
        self.user_1.refresh_from_db()
        self.user_2.refresh_from_db()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user_1.billing, 0.00)
        self.assertEqual(self.user_2.billing, 1500.00)

    def test_validation_if_sum_greater_than_sender_has(self):
        url = reverse("users:transfer-list")
        data = {
            'sender': self.user_1.id,
            'amount': 10000,
            'receiver': [self.user_2.inn]
        }
        response = self.client.post(
            url,
            data=data,
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertRaises(serializers.ValidationError)

    def test_sum_if_multiple_receivers(self):
        url = reverse("users:transfer-list")
        data = {
            'sender': self.user_1.id,
            'amount': 1000,
            'receiver': "{inn1}, {inn2}". format(
                inn1=self.user_2.inn,
                inn2=self.user_3.inn
            )
        }
        response = self.client.post(
            url,
            data=data,
        )
        self.user_1.refresh_from_db()
        self.user_2.refresh_from_db()
        self.user_3.refresh_from_db()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user_1.billing, 0.00)
        self.assertEqual(self.user_2.billing, 1000.00)
        self.assertEqual(self.user_3.billing, 600.00)

    def test_incorrect_receivers_inn(self):
        url = reverse("users:transfer-list")
        data = {
            'sender': self.user_1.id,
            'amount': 10000,
            'receiver': '111111111111'
        }
        response = self.client.post(
            url,
            data=data,
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertRaises(serializers.ValidationError)

    def test_get_list(self):
        url = reverse("users:transfer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
