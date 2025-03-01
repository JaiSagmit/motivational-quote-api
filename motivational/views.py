from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Quote
from .serializers import QuoteSerializer
import random

class RandomQuoteView(APIView):
    def get(self, request):
        random_quote = Quote.objects.order_by('?').first()  # Random quote
        serializer = QuoteSerializer(random_quote)
        return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Quote
from .serializers import QuoteSerializer
import random


# 1. Random Quote
class RandomQuoteView(APIView):
    def get(self, request):
        random_quote = Quote.objects.order_by('?').first()
        serializer = QuoteSerializer(random_quote)
        return Response(serializer.data)


# 2. Category-based Quotes
class CategoryQuoteView(APIView):
    def get(self, request, category):
        quotes = Quote.objects.filter(category=category)
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)


# 3. Author-based Quotes
class AuthorQuoteView(APIView):
    def get(self, request, authorName):
        quotes = Quote.objects.filter(author__icontains=authorName)
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)


# 4. Search Quotes (by keyword)
@api_view(['GET'])
def search_quotes(request):
    search_term = request.query_params.get('q', None)
    if search_term:
        quotes = Quote.objects.filter(text__icontains=search_term)
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)
    return Response({"message": "No search term provided."}, status=status.HTTP_400_BAD_REQUEST)


# 5. Daily Quote (one random quote per day)
@api_view(['GET'])
def daily_quote(request):
    random_quote = Quote.objects.order_by('?').first()
    serializer = QuoteSerializer(random_quote)
    return Response(serializer.data)


# 6. Mood-based Quotes
class MoodQuoteView(APIView):
    def get(self, request, mood):
        quotes = Quote.objects.filter(mood=mood)
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)


# 7. Positive Quotes
@api_view(['GET'])
def positive_quotes(request):
    quotes = Quote.objects.filter(category="positive")
    serializer = QuoteSerializer(quotes, many=True)
    return Response(serializer.data)


# 8. Inspirational Quotes
@api_view(['GET'])
def inspire_quotes(request):
    quotes = Quote.objects.filter(category="inspirational")
    serializer = QuoteSerializer(quotes, many=True)
    return Response(serializer.data)


# 9. Filter by Quote Length
@api_view(['GET'])
def length_quotes(request, length):
    if length == 'short':
        quotes = Quote.objects.filter(text__length__lte=100)
    elif length == 'medium':
        quotes = Quote.objects.filter(text__length__gte=101, text__length__lte=200)
    elif length == 'long':
        quotes = Quote.objects.filter(text__length__gte=201)
    else:
        return Response({"message": "Invalid length"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = QuoteSerializer(quotes, many=True)
    return Response(serializer.data)


# 10. Submit a New Quote (POST)
@api_view(['POST'])
def add_quote(request):
    serializer = QuoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Quote added successfully", "quoteId": serializer.data['id']},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 11. Update an Existing Quote (PUT)
@api_view(['PUT'])
def update_quote(request, quoteId):
    try:
        quote = Quote.objects.get(id=quoteId)
    except Quote.DoesNotExist:
        return Response({"message": "Quote not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuoteSerializer(quote, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Quote updated successfully", "quoteId": quoteId}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 12. Delete a Quote (DELETE)
@api_view(['DELETE'])
def delete_quote(request, quoteId):
    try:
        quote = Quote.objects.get(id=quoteId)
    except Quote.DoesNotExist:
        return Response({"message": "Quote not found"}, status=status.HTTP_404_NOT_FOUND)

    quote.delete()
    return Response({"message": "Quote deleted successfully", "quoteId": quoteId}, status=status.HTTP_204_NO_CONTENT)


# 13. Random Quote from Category
class RandomCategoryQuoteView(APIView):
    def get(self, request, category):
        random_quote = Quote.objects.filter(category=category).order_by('?').first()
        serializer = QuoteSerializer(random_quote)
        return Response(serializer.data)


# 14. Search Quotes by Author (Partial Match)
@api_view(['GET'])
def search_by_author(request):
    author_name = request.query_params.get('author', None)
    if author_name:
        quotes = Quote.objects.filter(author__icontains=author_name)
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)
    return Response({"message": "No author name provided."}, status=status.HTTP_400_BAD_REQUEST)


# 15. Filter by Length Range (Character count range)
@api_view(['GET'])
def length_range_quotes(request):
    min_length = int(request.query_params.get('min', 0))
    max_length = int(request.query_params.get('max', 500))
    quotes = Quote.objects.filter(text__length__gte=min_length, text__length__lte=max_length)
    serializer = QuoteSerializer(quotes, many=True)
    return Response(serializer.data)


# 16. Quotes by Theme
class ThemeQuoteView(APIView):
    def get(self, request, theme):
        quotes = Quote.objects.filter(theme=theme)
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)


# 17. Related Quotes to a Quote
class RelatedQuoteView(APIView):
    def get(self, request, quoteId):
        try:
            quote = Quote.objects.get(id=quoteId)
        except Quote.DoesNotExist:
            return Response({"message": "Quote not found"}, status=status.HTTP_404_NOT_FOUND)

        related_quotes = Quote.objects.filter(author=quote.author)  # Example: Same author
        serializer = QuoteSerializer(related_quotes, many=True)
        return Response(serializer.data)


# 18. Quotes by Celebrity
class CelebrityQuoteView(APIView):
    def get(self, request, celebrityName):
        quotes = Quote.objects.filter(celebrity__icontains=celebrityName)
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)


# 19. Popular Quotes (Most viewed, shared, or rated)
@api_view(['GET'])
def popular_quotes(request):
    quotes = Quote.objects.all().order_by('-views')  # Example: Sorted by views
    serializer = QuoteSerializer(quotes, many=True)
    return Response(serializer.data)


# 20. Weekly Quote Roundup
@api_view(['GET'])
def weekly_quotes(request):
    # You can implement logic to send a batch of 7 random quotes for a week
    quotes = Quote.objects.order_by('?')[:7]  # Select 7 random quotes for the week
    serializer = QuoteSerializer(quotes, many=True)
    return Response(serializer.data)
# quotes/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Quote
from .serializers import QuoteSerializer

# Example: Protecting the "add quote" view with authentication
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # This restricts the view to authenticated users
def add_quote(request):
    serializer = QuoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Quote added successfully", "quoteId": serializer.data['id']}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Example: Protecting the "update quote" view with authentication
@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # This restricts the view to authenticated users
def update_quote(request, quoteId):
    try:
        quote = Quote.objects.get(id=quoteId)
    except Quote.DoesNotExist:
        return Response({"error": "Quote not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuoteSerializer(quote, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Quote updated successfully", "quoteId": quoteId}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Example: Protecting the "delete quote" view with authentication
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # This restricts the view to authenticated users
def delete_quote(request, quoteId):
    try:
        quote = Quote.objects.get(id=quoteId)
    except Quote.DoesNotExist:
        return Response({"error": "Quote not found"}, status=status.HTTP_404_NOT_FOUND)

    quote.delete()
    return Response({"message": "Quote deleted successfully", "quoteId": quoteId}, status=status.HTTP_204_NO_CONTENT)
