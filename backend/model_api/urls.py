from django.urls import path
from .views import predict_heart_disease

urlpatterns = [
    path('predict/', predict_heart_disease, name='predict_heart_disease'),
]