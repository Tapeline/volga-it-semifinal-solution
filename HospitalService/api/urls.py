from django.urls import path

from . import views

urlpatterns = [
    path("Ping/", views.PingView.as_view()),
    path("Hospitals/", views.ListCreateHospitalView.as_view()),
    path("Hospitals/<int:pk>/", views.RetrieveUpdateDestroyHospitalView.as_view()),
    path("Hospitals/<int:pk>/rooms/", views.GetHospitalRoomsView.as_view()),
    path("Hospitals/Exists/<int:pk>/", views.HospitalExistsView.as_view()),
    path("Hospitals/RoomExists/<int:pk>/<str:room>/", views.HospitalRoomExistsView.as_view()),
]
