from django.shortcuts import render
from rest_framework import viewsets

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

from .serializers import UserSerializer, GroupSerializer


from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
