from rest_framework import serializers

from .models import HotelSearch


class HotelSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelSearch
        fields = [
            "id",
            "city_code",
            "check_in_date",
            "check_out_date",
            "adults",
            "result_count",
            "created_at",
        ]
        read_only_fields = ["id", "result_count", "created_at"]
