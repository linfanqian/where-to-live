from django.urls import path

from .views import SearchFormView, SearchResultView

urlpatterns = [
    path('search', SearchFormView.as_view(), name='search'),
    path('result', SearchResultView.as_view(), name='result'),
]