from rest_framework import serializers

class HeartInputSerializer(serializers.Serializer):
    # Fitur numerik dengan batas logis
    resting_bp = serializers.FloatField()
    fasting_bs = serializers.IntegerField()
    max_hr = serializers.FloatField()
    oldpeak = serializers.FloatField()

    # Fitur kategorikal dengan choices
    sex = serializers.ChoiceField(choices=['m', 'f'])
    resting_ecg = serializers.ChoiceField(choices=['normal', 'lvh', 'st'])
    exercise_angina = serializers.ChoiceField(choices=['y', 'n'])
    chest_pain_type = serializers.ChoiceField(choices=['ata', 'nap', 'asy', 'ta'])
    st_slope = serializers.ChoiceField(choices=['up', 'flat', 'down'])

    # Optional: case-insensitive validation
    def validate(self, data):
        for key in ['sex', 'resting_ecg', 'exercise_angina', 'chest_pain_type', 'st_slope']:
            data[key] = data[key].lower() 
        return data
