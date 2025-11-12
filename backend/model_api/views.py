import os
import pandas as pd
from catboost import CatBoostClassifier, Pool
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def predict_heart_disease(request):
    try:
        data = request.data
        df = pd.DataFrame([data])

        # Kolom kategorikal
        cat_features = ['sex', 'chest_pain_type', 'resting_ecg', 'exercise_angina', 'st_slope']

        # Pastikan kolom kategorikal bertipe string
        df[cat_features] = df[cat_features].astype(str)

        # Path absolut ke model
        MODEL_PATH = os.path.join(os.path.dirname(__file__), "catboost_model.cbm")

        # Load model
        model = CatBoostClassifier()
        model.load_model(MODEL_PATH)

        # Buat Pool dan prediksi
        pool = Pool(data=df, cat_features=cat_features)
        prediction = model.predict(pool)[0]
        proba = model.predict_proba(pool)[0][1]

        return Response({
            "prediction": int(prediction),
            "probability": float(proba)
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)
