from django import forms
from .models import Transfer
from django.contrib.auth import get_user_model

User = get_user_model()


class TransferForm(forms.ModelForm):

    receiver = forms.CharField(max_length=100)

    class Meta:
        model = Transfer
        fields = ('sender', 'receiver',  'amount',)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['sender'].billing - cleaned_data['amount'] >= 0:
            cleaned_data['sender'].billing -= cleaned_data['amount']
            cleaned_data['sender'].save()
            receivers_list = cleaned_data['receiver'].split(',')
            each_amount = cleaned_data['amount'] / len(receivers_list)
            receiver_users = list()
            for receiver in receivers_list:
                try:
                    one_receiver = User.objects.get(inn=receiver.strip())
                    one_receiver.billing += each_amount
                    one_receiver.save()
                    receiver_users.append(one_receiver)
                except User.DoesNotExist:
                    self.add_error(
                        'receiver',
                        'No INN {value} in db'.format(
                            value=receiver
                        )
                    )
            cleaned_data['receiver'] = receiver_users
        else:
            self.add_error(
                'amount',
                '{username} have only {value}$'.format(
                    username=cleaned_data['sender'].username,
                    value=cleaned_data['sender'].billing
                )
            )
        return cleaned_data
