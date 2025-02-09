from django.urls import path
from .views import DeckListCreateView, DeckDetailView, FlashcardListCreateView, FlashcardDetailView, SignupView, BulkFlashcardCreateView, BulkFlashcardDeleteView

urlpatterns = [
    path('decks/', DeckListCreateView.as_view(), name='deck-list-create'),
    path('decks/<int:pk>/', DeckDetailView.as_view(), name='deck-detail'),
    path('flashcards/', FlashcardListCreateView.as_view(), name='flashcard-list-create'),
    path('flashcards/<int:pk>/', FlashcardDetailView.as_view(), name='flashcard-detail'),
    # Endpoint for bulk flashcard creation
    path('flashcards/bulk_create/', BulkFlashcardCreateView.as_view(), name='flashcard-bulk-create'),
    path('flashcards/bulk_delete/', BulkFlashcardDeleteView.as_view(), name='flashcard-bulk-delete'),
    path('signup/', SignupView.as_view(), name='signup'),
]
