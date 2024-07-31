from django.db import models
from django.contrib.auth.models import User
from users.models import Student

book_category = [
    ('fiction', "Fiction"),
    ('programming', "Programming"),
    ('cooking', "Cooking"),
    ('story', 'Story'),
    ('history', 'History'),
    ('science', 'Science'),
]

class Book(models.Model):
    name = models.CharField(max_length=300)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=20, choices=book_category)
    author = models.CharField(max_length=150)
    image = models.ImageField(upload_to='book/')
    publication = models.CharField(max_length=150)
    description = models.TextField()
    quantity = models.PositiveBigIntegerField(default=0)
    availability = models.BooleanField(default=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    wishlist = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.availability = self.quantity > 0
        super().save(*args, **kwargs)


class BorrowedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    

    
    
