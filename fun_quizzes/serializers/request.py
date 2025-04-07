from rest_framework import serializers

class PastLifeTestRequestSerializer(serializers.Serializer):
    """
    전생 테스트 요청을 위한 시리얼라이저
    
    테스트 ID, 생년월일, 태어난 시간을 검증합니다.
    """
    test_id = serializers.IntegerField()
    birth_date = serializers.DateField(format="%Y-%m-%d")
    birth_time = serializers.TimeField(format="%H:%M")