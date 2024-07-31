from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('books/<int:book_pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('borrowed_books/<int:pk>/return/', views.return_book, name='return_book'),
    path('borrowed_books/', views.borrowed_books_list, name='borrowed_books_list'),
]
