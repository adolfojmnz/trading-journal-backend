from django.utils import timezone

from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data["username"])
            user.last_login = timezone.now()
            user.save()
        return response
