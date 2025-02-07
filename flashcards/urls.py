from django.urls import path
from .views import DeckListCreateView, DeckDetailView, FlashcardListCreateView, FlashcardDetailView

urlpatterns = [
    path('decks/', DeckListCreateView.as_view(), name='deck-list-create'),
    path('decks/<int:pk>/', DeckDetailView.as_view(), name='deck-detail'),
    path('flashcards/', FlashcardListCreateView.as_view(), name='flashcard-list-create'),
    path('flashcards/<int:pk>/', FlashcardDetailView.as_view(), name='flashcard-detail'),
]
