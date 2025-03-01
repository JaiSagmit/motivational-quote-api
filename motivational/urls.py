from django.urls import path
from .views import RandomQuoteView  # Import your view

urlpatterns = [
    path('quotes/random', RandomQuoteView.as_view(), name='random-quote'),
    # Add other routes for your other endpoints here
]
from django.urls import path
from .views import (
    RandomQuoteView, CategoryQuoteView, AuthorQuoteView, search_quotes, daily_quote,
    MoodQuoteView, positive_quotes, inspire_quotes, length_quotes, add_quote,
    update_quote, delete_quote, RandomCategoryQuoteView, search_by_author,
    length_range_quotes, ThemeQuoteView, RelatedQuoteView, CelebrityQuoteView,
    popular_quotes, weekly_quotes
)

urlpatterns = [
    path('quotes/random/', RandomQuoteView.as_view(), name='random-quote'),
    path('quotes/category/<str:category>/', CategoryQuoteView.as_view(), name='category-quote'),
    path('quotes/author/<str:authorName>/', AuthorQuoteView.as_view(), name='author-quote'),
    path('quotes/search/', search_quotes, name='search-quotes'),
    path('quotes/daily/', daily_quote, name='daily-quote'),
    path('quotes/mood/<str:mood>/', MoodQuoteView.as_view(), name='mood-quote'),
    path('quotes/positive/', positive_quotes, name='positive-quotes'),
    path('quotes/inspire/', inspire_quotes, name='inspire-quotes'),
    path('quotes/length/<str:length>/', length_quotes, name='length-quotes'),
    path('quotes/', add_quote, name='add-quote'),
    path('quotes/<int:quoteId>/', update_quote, name='update-quote'),
    path('quotes/delete/<int:quoteId>/', delete_quote, name='delete-quote'),
    path('quotes/random/<str:category>/', RandomCategoryQuoteView.as_view(), name='random-category-quote'),
    path('quotes/author/search/', search_by_author, name='search-by-author'),
    path('quotes/length-range/', length_range_quotes, name='length-range-quotes'),
    path('quotes/theme/<str:theme>/', ThemeQuoteView.as_view(), name='theme-quote'),
    path('quotes/related/<int:quoteId>/', RelatedQuoteView.as_view(), name='related-quote'),
    path('quotes/celebrity/<str:celebrityName>/', CelebrityQuoteView.as_view(), name='celebrity-quote'),
    path('quotes/popular/', popular_quotes, name='popular-quotes'),
    path('quotes/weekly/', weekly_quotes, name='weekly-quotes'),
]
# quotes/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import add_quote, update_quote, delete_quote

urlpatterns = [
    # Token Authentication Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token Obtain
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token Refresh

    # Your other API endpoints...
    path('quotes/', add_quote, name='add-quote'),
    path('quotes/<int:quoteId>/', update_quote, name='update-quote'),
    path('quotes/delete/<int:quoteId>/', delete_quote, name='delete-quote'),
]
