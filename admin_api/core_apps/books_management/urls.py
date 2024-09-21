from django.urls import path


from . import views

urlpatterns = [
    path("health-check/", views.HealthCheck.as_view(), name="Health-check"),
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]
