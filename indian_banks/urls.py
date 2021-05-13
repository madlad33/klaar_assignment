from django.urls import path, include
from .views import AutoCompleteView,SearchView

urlpatterns = [
    path('api/autocomplete', AutoCompleteView.as_view()),
    path('api/branches',SearchView.as_view())
]

