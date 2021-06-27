from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Transfer

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'inn', 'billing', 'password']

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class TransferSerializer(serializers.ModelSerializer):

    receiver = serializers.CharField(max_length=1000)

    class Meta:
        model = Transfer
        fields = ['id', 'sender', 'receiver', 'amount']

    def create(self, validated_data):
        if validated_data['sender'].billing - validated_data['amount'] >= 0:
            validated_data['sender'].billing -= validated_data['amount']
            validated_data['sender'].save()
            receivers_list = validated_data['receiver'].split(',')
            each_amount = validated_data['amount'] / len(receivers_list)
            receiver_users = list()
            for receiver in receivers_list:
                try:
                    one_receiver = User.objects.get(inn=receiver.strip())
                    one_receiver.billing += each_amount
                    one_receiver.save()
                    receiver_users.append(one_receiver)
                except User.DoesNotExist:
                    raise serializers.ValidationError(
                        'Пользователя с ИНН {value} нет в базе.'.format(
                            value=receiver
                        )
                    )
            validated_data['receiver'] = receiver_users
        else:
            raise serializers.ValidationError(
                'Не хватает средств'
            )
        return super().create(validated_data)
