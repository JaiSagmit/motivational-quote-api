from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Quote
import random


# ✅ User Services
def create_user(username, password):
    """Creates a new user with the given username and password."""
    user = User.objects.create_user(username=username, password=password)
    return user

def generate_tokens(user):
    """Generates JWT access and refresh tokens for the user."""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }

def authenticate_user(username, password):
    """Authenticates a user and returns JWT tokens if valid."""
    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        return generate_tokens(user)
    return None

# ✅ Quote Services
def add_quote(text, author=None, category=None):
    """Creates and saves a new quote in the database."""
    quote = Quote.objects.create(text=text, author=author, category=category)
    return quote

def get_random_quote():
    """Retrieves a random motivational quote from the database."""
    quotes = Quote.objects.all()
    if not quotes:
        return None
    return random.choice(quotes)