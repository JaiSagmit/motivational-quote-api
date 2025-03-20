from django.urls import path
from .views import RegisterView, LoginView, QuoteCreateView, RandomQuoteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('quotes/', QuoteCreateView.as_view(), name='add-quote'),
    path('quotes/random/', RandomQuoteView.as_view(), name='random-quote'),
]
