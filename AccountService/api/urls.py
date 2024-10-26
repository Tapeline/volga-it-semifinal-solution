from django.urls import path

from api import views

urlpatterns = [
    path("Ping/", views.PingView.as_view()),
    path("Authentication/SignUp/", views.RegisterView.as_view()),
    path("Authentication/SignIn/", views.LoginView.as_view()),
    path("Authentication/SignOut/", views.LogOutView.as_view()),
    path("Authentication/Validate/", views.ValidateTokenView.as_view()),
    path("Authentication/Refresh/", views.RefreshTokenView.as_view()),
    path("Accounts/Me/", views.ProfileView.as_view()),
    path("Accounts/Update/", views.UpdateMyProfileView.as_view()),
    path("Accounts/", views.ListCreateAllUsersView.as_view()),
    path("Accounts/<int:pk>/", views.UpdateDestroyUserView.as_view()),
    path("Accounts/Exists/<str:role>/<int:pk>/", views.UserExistsView.as_view()),
    path("Doctors/", views.ListDoctorsView.as_view()),
    path("Doctors/<int:pk>/", views.RetrieveDoctorView.as_view()),
]
