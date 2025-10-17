from django.apps import apps
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SentimentRequestSerializer

class SentimentPredictView(APIView):
    """
    API view to predict sentiment from a given text.
    """
    def post(self, request, *args, **kwargs):
        serializer = SentimentRequestSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            
            # Handle empty or whitespace-only input after validation
            if not text.strip():
                return Response({"error": "Input text cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Get the model from the AppConfig instance
                model = apps.get_app_config('sentiment_api').model
                
                # The model expects a list of texts for prediction
                prediction = model.predict([text])
                
                # The prediction is an array, get the first element
                raw_prediction = prediction[0]

                # Map the model output (1 for positive, 0 for negative) to a sentiment label
                if raw_prediction == 1:
                    sentiment = "Positive"
                else:
                    sentiment = "Negative"
                
                return Response({"sentiment": sentiment}, status=status.HTTP_200_OK)
            except Exception as e:
                # Handle any exceptions during prediction
                return Response({"error": f"An error occurred during prediction: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
