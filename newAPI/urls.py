from django.urls import path
from newAPI import views
from .models import *

urlpatterns = [
    # path('result/', Sentiment.as_view())
    path('index/<search>', views.index, name="index"),
    path('profile/<search>', views.profile, name="profile"),

]