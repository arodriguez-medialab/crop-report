from django.urls import path
from .views import LoadNdvisView, LoadHistoricalView, LoadHistoricalTmpView

urlpatterns = [
    path('load-ndvis', LoadNdvisView.as_view()),
    path('load-historical', LoadHistoricalView.as_view()),
    path('load-historical-tmp', LoadHistoricalTmpView.as_view()),
]