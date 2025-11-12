from rest_framework import serializers

class HeartInputSerializer(serializers.Serializer):
    resting_bp = serializers.FloatField()
    fasting_bs = serializers.FloatField()
    max_hr = serializers.FloatField()
    oldpeak = serializers.FloatField()
    sex = serializers.CharField()
    resting_ecg = serializers.CharField()
    exercise_angina = serializers.CharField()
    chest_pain_type = serializers.CharField()
    st_slope = serializers.CharField()
