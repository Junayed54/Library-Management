from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from books.models import Book, BorrowedBook, Student
from rest_framework.views import APIView




#user
class UserSignupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)




#books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]

class BorrowBookView(generics.CreateAPIView):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs['book_pk'])
        try:
            student = Student.objects.get(user=request.user)
            borrowed_books = BorrowedBook.objects.filter(student=student)
            if borrowed_books.exists():
                return Response(
                    {"detail": "You have already borrowed one book. Please return it before borrowing another."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Student.DoesNotExist:
            return Response(
                {"detail": "You are not authorized to borrow books."},
                status=status.HTTP_403_FORBIDDEN
            )

        if book.quantity > 0:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            borrowed_book = serializer.save(student=student, book=book)
            book.quantity -= 1
            if book.quantity == 0:
                book.availability = False
            book.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "This book is currently unavailable."}, status=status.HTTP_400_BAD_REQUEST)

class ReturnBookView(generics.UpdateAPIView):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        borrowed_book = get_object_or_404(BorrowedBook, pk=self.kwargs['pk'])
        student = Student.objects.get(user=request.user)
        if borrowed_book.student != student:
            return Response({"detail": "You are not authorized to return this book."}, status=status.HTTP_403_FORBIDDEN)

        borrowed_book.return_date = timezone.now()
        student.calculate_fine() 
        borrowed_book.save()
        borrowed_book.delete()

        book = borrowed_book.book
        book.quantity += 1
        book.availability = True
        book.save()

        return Response({"detail": "Book returned successfully."}, status=status.HTTP_200_OK)

class BorrowedBooksListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            student = Student.objects.get(id=request.user.id)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student matching query does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        borrowed_books = BorrowedBook.objects.filter(student=student)
        serializer = BorrowedBookSerializer(borrowed_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)