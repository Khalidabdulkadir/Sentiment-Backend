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
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            nltk.download('punkt_tab')

        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')

        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')

        # Load the model as before
        app_path = os.path.dirname(__file__)
        MODEL_PATH = os.path.join(app_path, 'sentiment_analysis.pkl')

        sys.modules['__main__'].TextCleaner = text_cleaner.TextCleaner
        self.model = joblib.load(MODEL_PATH)

