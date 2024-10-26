from django.urls import path

from . import views

urlpatterns = [
    path("Ping/", views.PingView.as_view()),
    path("History/Account/<int:pacient_id>/", views.ListHistoryForUserView.as_view()),
    path("History/<int:pk>/", views.RetrieveUpdateDocumentView.as_view()),
    path("History/", views.CreateDocumentView.as_view())
]
