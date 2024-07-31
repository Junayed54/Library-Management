from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Book, BorrowedBook
from .forms import BookForm, BorrowedBookForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from users.models import Student
from .models import BorrowedBook
def is_admin(user):
    return user.is_staff


def home(request):
    return render(request, template_name="home.html", context=None)




def book_list(request):
    books = Book.objects.all()
    return render(request, 'book.html', {'books': books})



def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})

    
@login_required
@user_passes_test(is_admin)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book_confirm_delete.html', {'book': book})



@login_required
def borrow_book(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    
    # Check if the logged-in user is a student
    try:
        student = Student.objects.get(user=request.user)
        borrowed_books = BorrowedBook.objects.filter(student=student)
        if borrowed_books.exists():
            message = "You have already borrowed one book. Please return it then borrow another."
            return HttpResponse(f"<h1>{message}</h1> <button style='background-color:orange;'><a href='/books/{book_pk}/'>Book Detail</a></button>")
    except Student.DoesNotExist:
        messages.error(request, "You are not authorized to borrow books.")
        return redirect('book_list')  # Redirect or handle unauthorized access
    
    if request.method == 'POST':
        form = BorrowedBookForm(request.POST)
        if form.is_valid():
            if book.quantity > 0:     
                borrowed_book = form.save(commit=False)
                borrowed_book.student = student
                borrowed_book.book = book
                borrowed_book.save()
                book.quantity -= 1
                if book.quantity == 0:
                    book.availability = False
                book.save()
                messages.success(request, "Book borrowed successfully.")
                return redirect('book_list')
            else:
                messages.error(request, "This book is currently unavailable.")
        else:
            messages.error(request, "There was an error with your form. Please try again.")
    else:
        form = BorrowedBookForm()
    
    return render(request, 'borrow_book_form.html', {'form': form, 'book': book})


@login_required
def return_book(request, pk):
    borrowed_book = get_object_or_404(BorrowedBook, pk=pk)
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':

        borrowed_book.return_date = timezone.now()
        student.calculate_fine()  # Calculate fine before saving
        borrowed_book.save()
        borrowed_book.delete()

        # Update book availability and quantity
        book = borrowed_book.book
        book.quantity += 1
        book.availability = True
        book.save()

        return redirect('borrowed_books_list')
    
    return render(request, 'return_book_form.html', {'borrowed_book': borrowed_book})

@login_required
def borrowed_books_list(request):
    student = Student.objects.get(user=request.user)
    borrowed_books = BorrowedBook.objects.filter(student=student)
    return render(request, 'borrowed_books_list.html', {'borrowed_books': borrowed_books})
