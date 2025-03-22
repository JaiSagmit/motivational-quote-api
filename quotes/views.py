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
from django.utils.timezone import now
from datetime import timedelta
import random
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError
from django.db.models.functions import Length
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.data.get("text")
        author = request.data.get("author", "").strip()
        category = request.data.get("category", "").strip()

        if not text:
            return Response({"error": "Quote text is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not author:
            return Response({"error": "Author name is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not category:
            return Response({"error": "Category is required"}, status=status.HTTP_400_BAD_REQUEST)


        quote = Quote.objects.create(text=text, author=author, category=category)

        return Response({
            "message": "Quote added successfully",
            "quoteId": quote.id,
            "author": quote.author,
            "category": quote.category,
            "theme": quote.theme
        }, status=status.HTTP_201_CREATED)

class RandomQuoteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quote = get_random_quote()
        if quote:
            serializer = QuoteSerializer(quote)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "No quotes available"}, status=status.HTTP_404_NOT_FOUND)

class QuoteByCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category):
        quotes = Quote.objects.filter(category__iexact=category)
        if quotes.exists():
            serializer = QuoteSerializer(quotes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "No quotes found for this category"}, status=status.HTTP_404_NOT_FOUND)

class QuoteByAuthorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, authorName):
        quotes = Quote.objects.filter(author__iexact=authorName)
        if quotes.exists():
            serializer = QuoteSerializer(quotes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "No quotes found for this author"}, status=status.HTTP_404_NOT_FOUND)

class QuoteSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        if not query:
            return Response({"error": "Search query is required"}, status=status.HTTP_400_BAD_REQUEST)


        quotes = Quote.objects.filter(
            text__icontains=query
        ) | Quote.objects.filter(
            category__icontains=query
        )

        if quotes.exists():
            serializer = QuoteSerializer(quotes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": "No matching quotes found"}, status=status.HTTP_404_NOT_FOUND)

class DailyQuoteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        today = now().date()
        quote = Quote.objects.filter(created_at__date=today).first()

        if not quote:

            quote = Quote.objects.order_by("?").first()

        if quote:
            serializer = QuoteSerializer(quote)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": "No quotes available"}, status=status.HTTP_404_NOT_FOUND)

class QuoteByMoodView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, mood):
        quotes = Quote.objects.filter(category__iexact=mood)
        if quotes.exists():
            serializer = QuoteSerializer(quotes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "No quotes found for this mood"}, status=status.HTTP_404_NOT_FOUND)

class PositiveQuotesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        positive_keywords = ["positive", "happiness", "joy", "optimism", "inspiration", "uplifting"]
        quotes = Quote.objects.filter(category__in=positive_keywords)

        if quotes.exists():
            serializer = QuoteSerializer(quotes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "No positive quotes available"}, status=status.HTTP_404_NOT_FOUND)

class InspireQuoteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quotes = Quote.objects.filter(category__iexact="inspiration")
        if quotes.exists():
            serializer = QuoteSerializer(quotes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "No inspiring quotes available"}, status=status.HTTP_404_NOT_FOUND)


from django.db.models.functions import Length

class QuoteByLengthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, length):

        quotes = Quote.objects.annotate(text_length=Length('text'))

        if length == "short":
            quotes = quotes.filter(text_length__lte=50)
        elif length == "medium":
            quotes = quotes.filter(text_length__gt=50, text_length__lte=150)
        elif length == "long":
            quotes = quotes.filter(text_length__gt=150)
        else:
            return Response({"error": "Invalid length type. Use 'short', 'medium', or 'long'."},
                            status=status.HTTP_400_BAD_REQUEST)

        if quotes.exists():
            serializer = QuoteSerializer(quotes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": f"No {length} quotes available"}, status=status.HTTP_404_NOT_FOUND)


class QuoteUpdateView(UpdateAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):

        try:
            quote = self.get_object()
            serializer = self.get_serializer(quote, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Quote updated successfully", "quoteId": quote.id},
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Quote.DoesNotExist:
            return Response({"message": "Quote not found"}, status=status.HTTP_404_NOT_FOUND)

class QuoteDeleteView(DestroyAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        quote = self.get_object()
        self.perform_destroy(quote)
        return Response({"message": "Quote deleted successfully"}, status=status.HTTP_200_OK)

class RandomQuoteByCategoryView(APIView):


    def get(self, request, category):
        quotes = Quote.objects.filter(category__iexact=category)

        if quotes.exists():
            random_quote = random.choice(quotes)
            serializer = QuoteSerializer(random_quote)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": f"No quotes found in the '{category}' category"}, status=status.HTTP_404_NOT_FOUND)


class QuoteByLengthRangeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            min_length = int(request.query_params.get("min", 0))
            max_length = int(request.query_params.get("max", 9999))

            if min_length < 0 or max_length < 0:
                return Response({"error": "Length values must be non-negative"}, status=status.HTTP_400_BAD_REQUEST)

            quotes = Quote.objects.annotate(text_length=Length("text")).filter(
                text_length__gte=min_length, text_length__lte=max_length
            )

            if quotes.exists():
                serializer = QuoteSerializer(quotes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": f"No quotes found in the {min_length}-{max_length} character range"},
                            status=status.HTTP_404_NOT_FOUND)

        except ValueError:
            return Response({"error": "Invalid query parameters. Please provide numeric values for min and max."},
                            status=status.HTTP_400_BAD_REQUEST)

class QuoteByThemeView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, theme):
        quotes = Quote.objects.filter(theme__iexact=theme).exclude(theme__isnull=True)

        if quotes:
            serializer = QuoteSerializer(quotes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"message": f"No quotes found for theme '{theme}'."},
            status=status.HTTP_404_NOT_FOUND
        )

class RelatedQuotesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, quoteId):

        quote = get_object_or_404(Quote, id=quoteId)


        related_quotes = Quote.objects.filter(
            theme=quote.theme
        ).exclude(id=quote.id) | Quote.objects.filter(
            author=quote.author
        ).exclude(id=quote.id)


        if related_quotes.exists():
            serializer = QuoteSerializer(related_quotes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"message": "No related quotes found."},
            status=status.HTTP_404_NOT_FOUND
        )


class QuotesByCelebrityView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, celebrityName):
        quotes = Quote.objects.filter(author__iexact=celebrityName)

        if quotes.exists():
            serializer = QuoteSerializer(quotes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": f"No quotes found for celebrity '{celebrityName}'"}, status=status.HTTP_404_NOT_FOUND)

class PopularQuotesView(APIView):


    def get(self, request):
        popular_quotes = Quote.objects.order_by('-views', '-shares', '-rating')[:10]
        serializer = QuoteSerializer(popular_quotes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WeeklyQuoteView(APIView):


    def get(self, request):

        today = now().date()


        start_of_week = today - timedelta(days=today.weekday())


        end_of_week = start_of_week + timedelta(days=6)


        weekly_quotes = Quote.objects.filter(
            created_at__date__gte=start_of_week, created_at__date__lte=end_of_week
        )


        if weekly_quotes.exists():
            serializer = QuoteSerializer(weekly_quotes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


        return Response({"message": "No quotes found for this week."}, status=status.HTTP_404_NOT_FOUND)


class AuthorSearchView(APIView):

    def get(self, request):

        author_name = request.query_params.get('author', '').strip()

        print(f"Searching for author: {author_name}")


        if author_name:

            quotes = Quote.objects.filter(author__icontains=author_name)


            if quotes.exists():
                serializer = QuoteSerializer(quotes, many=True)
                return Response(serializer.data)
            else:

                return Response({"message": "No quotes found for this author."}, status=404)
        else:

            return Response({"message": "Please provide an author name."}, status=400)