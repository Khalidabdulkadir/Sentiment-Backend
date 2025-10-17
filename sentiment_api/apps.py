from django.apps import AppConfig


import os
import sys
import joblib
import nltk
from django.conf import settings
from . import text_cleaner

class SentimentApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sentiment_api"

    model = None  # Initialize a placeholder for the model

    def ready(self):
        # This method is called once when the app is ready.

        # Download NLTK data required for the TextCleaner
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')

        # Path to the trained model, relative to this app's directory
        app_path = os.path.dirname(__file__)
        MODEL_PATH = os.path.join(app_path, 'sentiment_analysis.pkl')

        # This is the 'monkey patch'. It manually injects the TextCleaner class
        # into the __main__ module, which is where pickle is looking for it.
        sys.modules['__main__'].TextCleaner = text_cleaner.TextCleaner

        # Load the model and store it on the AppConfig instance
        self.model = joblib.load(MODEL_PATH)
