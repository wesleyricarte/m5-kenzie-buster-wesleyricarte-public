from rest_framework import serializers
from movies.models import Movie, RatingChoices, MovieOrder
from users.serializers import UserSerializer


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(
        max_length=10,
        allow_null=True,
        default=None,
    )
    rating = serializers.ChoiceField(
        allow_null=True,
        choices=RatingChoices.choices,
        default=RatingChoices.G,
    )
    synopsis = serializers.CharField(
        allow_null=True,
        default=None,
    )

    added_by = serializers.SerializerMethodField(read_only=True)

    def get_added_by(self, mov: Movie):
        return mov.user.email

    def create(self, validated_data: dict) -> Movie:
        return Movie.objects.create(**validated_data)


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_by = serializers.SerializerMethodField(read_only=True)
    buyed_at = serializers.DateTimeField(read_only=True)

    def get_title(self, mov: MovieOrder):
        return mov.movie.title

    def get_buyed_by(self, mov: MovieOrder):
        return mov.user.email

    def create(self, validated_data: dict) -> MovieOrder:
        return MovieOrder.objects.create(**validated_data)
