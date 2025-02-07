from rest_framework import serializers
from .models import Deck, Flashcard

# Serializers for converting model instances to JSON and vice versa
class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = '__all__'  # Include all fields

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = '__all__'  # Include all fields
