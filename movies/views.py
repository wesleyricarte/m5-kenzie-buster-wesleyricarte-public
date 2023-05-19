from rest_framework.views import APIView, Request, Response, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404

from movies.models import Movie
from movies.serializers import MovieSerializer, MovieOrderSerializer
from movies.permissions import MyCustomPermission


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyCustomPermission]

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()
        movies_paged = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerializer(instance=movies_paged, many=True)

        return self.get_paginated_response(serializer.data)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyCustomPermission]

    def get(self, req: Request, movie_id: int) -> Response:
        movie_found = get_object_or_404(klass=Movie, pk=movie_id)
        serializer = MovieSerializer(movie_found)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, req: Request, movie_id: int) -> Response:
        movie_found = get_object_or_404(klass=Movie, pk=movie_id)
        movie_found.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, req: Request, movie_id: int) -> Response:
        movie_found = get_object_or_404(klass=Movie, pk=movie_id)

        serializer = MovieOrderSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(movie=movie_found, user=req.user)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
