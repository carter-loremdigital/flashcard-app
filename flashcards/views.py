from django.shortcuts import render
from rest_framework import generics, permissions, views, response, status
from .models import Deck, Flashcard
from .serializers import DeckSerializer, FlashcardSerializer, UserSignupSerializer

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

    # Filter cards by deck
    def get_queryset(self):
        # Start with flashcards belonging to the authenticated user
        queryset = Flashcard.objects.filter(owner=self.request.user)
        # Check for a "deck" query parameter in the URL
        deck_id = self.request.query_params.get('deck')
        if deck_id:
            queryset = queryset.filter(deck__id=deck_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FlashcardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    permission_classes = [permissions.IsAuthenticated]

# Class for creating cards in bulk (e.g. when creating a new deck)
class BulkFlashcardCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Expects request.data to be a list of flashcard objects.
        Each flashcard object should include at least the 'question', 'answer',
        and a 'deck' field (which is the deck's id to which the flashcard should be linked).
        """
        # Validate incoming data with the FlashcardSerializer (with many=True)
        serializer = FlashcardSerializer(data=request.data, many=True)
        if serializer.is_valid():
            # Extract validated data
            flashcards_data = serializer.validated_data

            # Build Flashcard instances, ensuring that the owner is set to the current user.
            flashcards = []
            for data in flashcards_data:
                # Override the owner field so that the user cannot set it arbitrarily.
                flashcards.append(Flashcard(
                    question=data["question"],
                    answer=data["answer"],
                    deck=data["deck"],  # Ensure the client includes the deck id, or you can obtain it from kwargs.
                    owner=request.user
                ))

            # Use bulk_create for efficiency.
            Flashcard.objects.bulk_create(flashcards)
            return response.Response(
                {"message": "Flashcards created successfully."},
                status=status.HTTP_201_CREATED
            )
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Endpoint for deleting cards in bulk (e.g. when saving an edited deck)
class BulkFlashcardDeleteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        deck_id = request.query_params.get('deck')
        if not deck_id:
            return response.Response({"error": "Deck id is required."}, status=status.HTTP_400_BAD_REQUEST)
        # Delete all flashcards for this deck owned by the current user
        Flashcard.objects.filter(deck=deck_id, owner=request.user).delete()
        return response.Response({"message": "Flashcards deleted successfully."}, status=status.HTTP_200_OK)


# Authentication views
class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]