import re
import string
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class TextCleaner(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        text = str(text).lower()
        text = re.sub(r'http\S+|www\S+', '', text)  # Remove URLs
        text = re.sub(r'@\w+', '', text)  # Remove mentions
        text = re.sub(r'#', '', text)  # Remove hashtags symbol
        text = re.sub(r'\d+', '', text)  # Remove numbers
        text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
        tokens = word_tokenize(text)
        tokens = [t for t in tokens if t not in self.stop_words]  # Remove stopwords
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens]  # Lemmatize
        return ' '.join(tokens)

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Apply the cleaning function to each item in the input list
        return [self.clean_text(text) for text in X]
