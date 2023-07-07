from django.urls import path

from .views import SearchFormView, SearchResultView
from .views import SubscribeView

urlpatterns = [
    path('search', SearchFormView.as_view(), name='search'),
    path('result', SearchResultView.as_view(), name='result'),
    path('subscribe', SubscribeView.as_view(), name='subscribe'),
]