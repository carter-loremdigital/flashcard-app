from django.test import TestCase

# Database testing imports
from django.contrib.auth import get_user_model
from django.core.management import call_command
from flashcards.models import Deck, Flashcard

# Rate limit testing imports
from rest_framework.test import APIClient
from django.urls import reverse

User = get_user_model()

# Test wiping the database
class WipeDemoCommandTest(TestCase):
    def setUp(self):
        # Create a superuser (this account should be preserved)
        self.superuser = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        # Create some non-superuser users
        self.user1 = User.objects.create_user(username="user1", password="pass1")
        self.user2 = User.objects.create_user(username="user2", password="pass2")

        # Create decks for user1
        self.deck1 = Deck.objects.create(name="Deck 1", description="Test deck 1", owner=self.user1)
        self.deck2 = Deck.objects.create(name="Deck 2", description="Test deck 2", owner=self.user1)
        # Create flashcards for deck1
        self.flashcard1 = Flashcard.objects.create(question="What is 1+1?", answer="2", deck=self.deck1, owner=self.user1)
        self.flashcard2 = Flashcard.objects.create(question="What is the capital of France?", answer="Paris", deck=self.deck1, owner=self.user1)
        
        # Create decks and flashcards for user2
        self.deck3 = Deck.objects.create(name="Deck 3", description="Test deck 3", owner=self.user2)
        self.flashcard3 = Flashcard.objects.create(question="What is 2+2?", answer="4", deck=self.deck3, owner=self.user2)
        self.flashcard4 = Flashcard.objects.create(question="What color is the sky?", answer="Blue", deck=self.deck3, owner=self.user2)

    def test_demo_data_present(self):
        """
        Verify that the demo data is created as expected.
        """
        # We should have 2 non-superuser users.
        self.assertEqual(User.objects.filter(is_superuser=False).count(), 2)
        # And 3 decks in total.
        self.assertEqual(Deck.objects.count(), 3)
        # And 4 flashcards in total.
        self.assertEqual(Flashcard.objects.count(), 4)

    def test_wipe_database_command(self):
        """
        Run the wipe_database management command and ensure that non-superuser data is removed.
        """
        # Run the custom management command.
        call_command("wipe_database")

        # After wiping, there should be no non-superuser users.
        self.assertEqual(User.objects.filter(is_superuser=False).count(), 0)
        # With non-superusers removed, decks and flashcards should be gone (due to cascade deletion).
        self.assertEqual(Deck.objects.count(), 0)
        self.assertEqual(Flashcard.objects.count(), 0)
        # The superuser should still be present.
        self.assertEqual(User.objects.filter(is_superuser=True).count(), 1)

# Test API rate limit
class RateLimitTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        
        # Initialize APIClient and force authentication for the test user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Get the URL for an endpoint that is rate-limited (e.g., the deck list/create endpoint)
        self.url = reverse('deck-list-create')

    def test_rate_limiting_for_authenticated_users(self):
        """
        Simulate a series of requests from an authenticated user and assert that
        once the throttle limit is reached, a 429 (Too Many Requests) response is returned.
        For testing, assume the user rate throttle is set low (e.g., 5 requests per minute).
        """
        response_status = 200

        # Loop over a number of requests; if your throttle is 5/minute, try 10 requests.
        for i in range(10):
            response = self.client.get(self.url)
            response_status = response.status_code
            # If we hit the rate limit, break out of the loop.
            if response_status == 429:
                break

        # Assert that we eventually receive a 429 response.
        self.assertEqual(
            response_status, 429,
            f"Expected 429 status code after rate limiting, got {response_status} instead."
        )

class AnonymousRateLimitTest(TestCase):
    def setUp(self):
        # Initialize an API client for anonymous requests
        self.client = APIClient()
        # Assume that the signup endpoint is publicly accessible and has a URL name of 'signup'
        self.url = reverse('signup')

    def test_anonymous_rate_limiting(self):
        """
        Repeatedly call the signup endpoint as an anonymous user.
        Expect that after a number of requests the rate limit is exceeded, resulting in a 429 response.
        """
        response_status = 200

        # Make, for example, 10 requests; adjust as needed to exceed your throttle limit.
        for i in range(10):
            payload = {
                # Generate a unique username for each request to avoid duplicate errors
                "username": f"anonymous_test_{i}",
                "password": "testpass123"
            }
            response = self.client.post(self.url, payload, format="json")
            response_status = response.status_code

            # If we get a 429 status code, break out early.
            if response_status == 429:
                break

        # Assert that eventually we receive a 429 Too Many Requests response.
        self.assertEqual(
            response_status, 429,
            f"Expected 429 status code after rate limiting, got {response_status} instead."
        )