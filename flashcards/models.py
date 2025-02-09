from django.db import models
from django.contrib.auth import get_user_model

# Use Django's built-in user model
User = get_user_model()

class Deck(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='decks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Flashcard(models.Model):
    question = models.TextField()
    answer = models.TextField()
    deck = models.ForeignKey(
        Deck, on_delete=models.CASCADE, related_name='flashcards'
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='flashcards'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Flashcard in {self.deck.name}"
