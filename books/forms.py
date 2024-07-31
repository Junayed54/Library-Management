from django import forms
from .models import Book, BorrowedBook

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'isbn', 'category', 'author', 'image', 'publication', 'description', 'quantity', 'availability']

class BorrowedBookForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = ['due_date']
