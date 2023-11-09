from django.urls import path
from shoes import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('card/', views.CardView.as_view(), name="card"),
]