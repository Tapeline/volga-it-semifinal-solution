from django.urls import path

from . import views

urlpatterns = [
    path("Ping/",
         views.PingView.as_view()),
    path("Timetable/",
         views.CreateTimetableView.as_view()),
    path("Timetable/<int:pk>/",
         views.UpdateDestroyTimetableView.as_view()),
    path("Timetable/Doctor/<int:doctor_id>/",
         views.RetrieveDeleteTimetablesByDoctorId.as_view()),
    path("Timetable/Hospital/<int:hospital_id>/",
         views.RetrieveDeleteTimetablesByHospitalId.as_view()),
    path("Timetable/Hospital/<int:hospital_id>/Room/<str:room>/",
         views.RetrieveDeleteTimetablesByRoomView.as_view()),
    path("Timetable/<int:pk>/Appointments/",
         views.AppointmentsView.as_view()),
    path("Appointment/<int:pk>/",
         views.DeleteAppointmentView.as_view()),
]
