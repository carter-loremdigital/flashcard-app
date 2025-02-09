from rest_framework import serializers
from .models import Deck, Flashcard
from django.contrib.auth import get_user_model

# Serializers for converting model instances to JSON and vice versa
class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = '__all__'  # Include all fields
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = '__all__' 
        read_only_fields = ('id', 'owner', 'created_at')

User = get_user_model()
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        # Use create_user to ensure the password is hashed
        user = User.objects.create_user(**validated_data)
        return user