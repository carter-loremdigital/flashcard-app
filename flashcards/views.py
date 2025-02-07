from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Deck, Flashcard
from .serializers import DeckSerializer, FlashcardSerializer

# Create your views here.

# Django REST Framework generic views - simplify CRUD operations w/ built-in Django views
# Deck Views
class DeckListCreateView(generics.ListCreateAPIView):
    serializer_class = DeckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only decks owned by the authenticated user
        return Deck.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the deck with the logged-in user
        serializer.save(owner=self.request.user)

class DeckDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow access to decks owned by the logged-in user
        return Deck.objects.filter(owner=self.request.user)


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