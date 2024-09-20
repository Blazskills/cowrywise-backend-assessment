from django.urls import path


from . import views

urlpatterns = [
    path("frontend-health-check/", views.HealthCheck.as_view(), name="Health-check"),
    path('users/', views.UserCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]