from django.urls import path
from .views import SentimentPredictView

urlpatterns = [
    path('predict/', SentimentPredictView.as_view(), name='sentiment-predict'),
]
