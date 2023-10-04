from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from user_profile.serializers import UserSerializer


class ListUsersAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
