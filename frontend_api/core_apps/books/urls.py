from django.urls import path


from . import views

urlpatterns = [
    path("frontend-health-check/", views.HealthCheck.as_view(), name="Health-check"),
    path('users/', views.UserCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('books/', views.BookListAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),


    path('borrow/', views.BorrowBookAPIView.as_view(), name='borrow-create'),
    path('borrow/<int:pk>/', views.BorrowBookAPIView.as_view(), name='borrow-update'),

]
