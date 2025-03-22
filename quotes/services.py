from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Quote
import random



def create_user(username, password):

    user = User.objects.create_user(username=username, password=password)
    return user

def generate_tokens(user):

    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }

def authenticate_user(username, password):

    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        return generate_tokens(user)
    return None


def add_quote(text, author=None, category=None):

    quote = Quote.objects.create(text=text, author=author, category=category)
    return quote

def get_random_quote():

    quotes = Quote.objects.all()
    if not quotes:
        return None
    return random.choice(quotes)