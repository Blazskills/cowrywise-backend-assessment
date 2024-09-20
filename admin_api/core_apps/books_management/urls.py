from django.urls import path


from . import views

urlpatterns = [
    path("health-check/", views.HealthCheck.as_view(), name="Health-check"),
]
