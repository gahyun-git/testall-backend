from rest_framework import serializers

class PastLifeTestRequestSerializer(serializers.Serializer):
    """
    전생 테스트 요청을 위한 시리얼라이저
    """
    birth_date = serializers.DateField(
        format="%Y-%m-%d",
        input_formats=["%Y-%m-%d"],
        required=True
    )
    birth_time = serializers.TimeField(
        format="%H:%M",
        input_formats=["%H:%M"],
        required=True
    )
    is_time_unknown = serializers.BooleanField(required=False, default=False)