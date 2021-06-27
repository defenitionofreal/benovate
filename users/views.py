from .serializers import CustomUserSerializer, TransferSerializer
from django.contrib.auth import get_user_model
from .models import Transfer
from .forms import TransferForm
from django.views.generic import CreateView, ListView, DetailView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)


class TransferViewSet(viewsets.ModelViewSet):

    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = (AllowAny,)


class UserListView(ListView):

    model = User
    template_name = 'users_list.html'

    def get_context_data(self, **kwargs):
        ctx = super(UserListView, self).get_context_data(**kwargs)
        ctx['users'] = User.objects.all()
        return ctx


class UserDetailView(DetailView):

    model = User
    form_class = TransferForm
    template_name = 'user_detail.html'


class TransferCreateView(CreateView):

    model = Transfer
    form_class = TransferForm
    template_name = 'transfer_form.html'
    success_url = '.'

    def get_context_data(self, **kwargs):
        ctx = super(TransferCreateView, self).get_context_data(**kwargs)
        ctx['transfers'] = Transfer.objects.all()
        return ctx


def index_redirect(request):
    return redirect('users:user-list')