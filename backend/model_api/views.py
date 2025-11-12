from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from catboost import CatBoostClassifier
from .serializers import HeartInputSerializer
import requests

# Load model
model = CatBoostClassifier()
model.load_model("model_api/catboost/catboost_model.cbm")

GOOGLE_SHEET_WEBHOOK = "https://script.google.com/macros/s/AKfycbyxAIKkFwKpQ5l7X6BPc8SqHkHNyOZ1zn9d4PPo4dBkbuWUygHIkIJLrcQT_IaOosMh/exec"

@api_view(['POST'])
def predict_heart_disease(request):
    serializer = HeartInputSerializer(data=request.data)
    
    # Validasi input
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data

    try:
        # ML input
        X = [[
            validated_data['sex'],
            validated_data['chest_pain_type'],
            validated_data['resting_bp'],
            validated_data['fasting_bs'],
            validated_data['resting_ecg'],
            validated_data['max_hr'],
            validated_data['exercise_angina'],
            validated_data['oldpeak'],
            validated_data['st_slope']
        ]]

        # Prediksi
        prob = model.predict_proba(X)[0][1]
        pred = int(model.predict(X)[0])
        result = "Heart Disease" if pred == 1 else "No Heart Disease"

        # Kirim ke Google Spreadsheet
        requests.post(GOOGLE_SHEET_WEBHOOK, json={ 
            "sex": validated_data['sex'], 
            "chest_pain_type": validated_data['chest_pain_type'], 
            "resting_bp": validated_data['resting_bp'], 
            "fasting_bs": validated_data['fasting_bs'], 
            "resting_ecg": validated_data['resting_ecg'], 
            "max_hr": validated_data['max_hr'], 
            "exercise_angina": validated_data['exercise_angina'], 
            "oldpeak": validated_data['oldpeak'], 
            "st_slope": validated_data['st_slope'], 
            "result_predict": result, 
            "probability": round(float(prob), 4) })

        return Response({
            "Prediction": result,
            "Probability": round(float(prob), 4)
        })

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
