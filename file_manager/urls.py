from django.urls import path
from .views import LoadNdviFileView

urlpatterns = [
    path('load-ndvi-file', LoadNdviFileView.as_view()),
]