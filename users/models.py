from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date


class Student(models.Model):
    fullname = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    joined_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    grade = models.CharField(max_length=10)
    enrollment_status = models.BooleanField(default=True)
    emergency_contact = models.CharField(max_length=150)
    notes = models.TextField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    fine_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.fullname
    

    def calculate_fine(self):
        if self.return_date and isinstance(self.return_date, datetime):
            return_date_as_date = self.return_date.date()
        else:
            return_date_as_date = self.return_date
        
        if return_date_as_date and return_date_as_date > self.due_date:
            days_overdue = (return_date_as_date - self.due_date).days
            fine_rate_per_day = 2.0  # Example: $2 per day
            self.fine_amount = days_overdue * fine_rate_per_day
        else:
            self.fine_amount = 0.0

    def save(self, *args, **kwargs):
        self.calculate_fine()
        super().save(*args, **kwargs)
