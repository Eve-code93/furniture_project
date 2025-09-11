from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.CustomerListView.as_view(), name='customer-list'),  # optional
    path('me/', views.CustomerProfileView.as_view(), name='customer-profile'),
]
