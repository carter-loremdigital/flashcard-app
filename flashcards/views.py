from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Deck, Flashcard
from .serializers import DeckSerializer, FlashcardSerializer

# Create your views here.

# Django REST Framework generic views - simplify CRUD operations w/ built-in Django views
# Deck Views
class DeckListCreateView(generics.ListCreateAPIView):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Associate with logged-in user

class DeckDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer
    permission_classes = [permissions.IsAuthenticated]


# Flashcard Views
class FlashcardListCreateView(generics.ListCreateAPIView):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FlashcardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    permission_classes = [permissions.IsAuthenticated]