from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """ Custom user model """
    inn = models.CharField('INN', max_length=12, unique=True,
                           null=True, blank=True, default=0)
    billing = models.DecimalField(
        'Balance', max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return self.username


class Transfer(models.Model):
    """ Transfer balance model """
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ManyToManyField(CustomUser, related_name='receiver')
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
