from rest_framework import serializers

class SentimentRequestSerializer(serializers.Serializer):
    text = serializers.CharField(allow_blank=False, trim_whitespace=True)
