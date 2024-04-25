from django.urls import path
from . import views

app_name = 'check_processor'

urlpatterns = [
    path('places/', views.PlaceListView.as_view(), name='place_list'),
    path('analytics/', views.TotalAnalyticsView.as_view(), name='total_analytics'),
]
