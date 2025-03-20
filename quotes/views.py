from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, QuoteSerializer
from .models import Quote
from .services import get_random_quote
from .services import add_quote

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
class QuoteCreateView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Requires JWT authentication

    def post(self, request):
        text = request.data.get("text")
        author = request.data.get("author", None)
        category = request.data.get("category", None)

        if not text:
            return Response({"error": "Quote text is required"}, status=status.HTTP_400_BAD_REQUEST)

        quote = add_quote(text, author, category)

        return Response({
            "message": "Quote added successfully",
            "quoteId": quote.id
        }, status=status.HTTP_201_CREATED)

class RandomQuoteView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Requires JWT authentication

    def get(self, request):
        quote = get_random_quote()
        if quote:
            serializer = QuoteSerializer(quote)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "No quotes available"}, status=status.HTTP_404_NOT_FOUND)