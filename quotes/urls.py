from django.urls import path
from .views import RegisterView, LoginView, QuoteCreateView, RandomQuoteView, QuoteByCategoryView, QuoteByAuthorView, QuoteSearchView, DailyQuoteView, QuoteByMoodView, PositiveQuotesView, InspireQuoteView, QuoteByLengthView, QuoteUpdateView, QuoteDeleteView, RandomQuoteByCategoryView, QuoteByLengthRangeView, QuoteByThemeView, RelatedQuotesView, QuotesByCelebrityView, PopularQuotesView, WeeklyQuoteView, AuthorSearchView

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('quotes/', QuoteCreateView.as_view(), name='add-quote'),
    path('quotes/random/', RandomQuoteView.as_view(), name='random-quote'),
    path('quotes/category/<str:category>/', QuoteByCategoryView.as_view(), name='quote-by-category'),
    path('quotes/author/<str:authorName>/', QuoteByAuthorView.as_view(), name='quote-by-author'),
    path('quotes/search/', QuoteSearchView.as_view(), name='quote-search'),
    path('quotes/daily/', DailyQuoteView.as_view(), name='daily-quote'),
    path('quotes/mood/<str:mood>/', QuoteByMoodView.as_view(), name='quote-by-mood'),
    path('quotes/positive/', PositiveQuotesView.as_view(), name='positive-quotes'),
    path('quotes/inspire/', InspireQuoteView.as_view(), name='inspire-quote'),
    path('quotes/length/<str:length>/', QuoteByLengthView.as_view(), name='quote-by-length'),
    path('quotes/<int:pk>/', QuoteUpdateView.as_view(), name='quote-update'),
    path('quotes/<int:pk>/delete/', QuoteDeleteView.as_view(), name='quote-delete'),
    path('quotes/random/<str:category>/', RandomQuoteByCategoryView.as_view(), name='random-quote-by-category'),
    path('quotes/length-range/', QuoteByLengthRangeView.as_view(), name='quote-length-range'),
    path('quotes/theme/<str:theme>/', QuoteByThemeView.as_view(), name='quote-by-theme'),
    path('quotes/related/<int:quoteId>/', RelatedQuotesView.as_view(), name='related-quotes'),
    path('quotes/celebrity/<str:celebrityName>/', QuotesByCelebrityView.as_view(), name='quotes-by-celebrity'),
    path('quotes/popular/', PopularQuotesView.as_view(), name='popular-quotes'),
    path('quotes/weekly/', WeeklyQuoteView.as_view(), name='weekly-quotes'),
    path('api/quotes/author/search/', AuthorSearchView.as_view(), name='author_search'),
]
