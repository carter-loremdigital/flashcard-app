from django.contrib import admin
from .models import Deck, Flashcard

# Register models
admin.site.register(Deck)
admin.site.register(Flashcard)