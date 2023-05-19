from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsUserOrEmployee


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUserOrEmployee]

    def get(self, request: Request, user_id: int) -> Response:
        user_found = get_object_or_404(klass=User, id=user_id)
        self.check_object_permissions(request=request, obj=user_found)
        serializer = UserSerializer(user_found)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int) -> Response:
        user_found = get_object_or_404(klass=User, id=user_id)
        self.check_object_permissions(request=request, obj=user_found)

        serializer = UserSerializer(
            instance=user_found,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)
