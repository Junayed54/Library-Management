# Generated by Django 5.0.6 on 2024-07-16 07:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_alter_student_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('isbn', models.CharField(max_length=20, unique=True)),
                ('category', models.CharField(choices=[('fiction', 'Fiction'), ('programming', 'Programming'), ('cooking', 'Cooking'), ('story', 'Story'), ('history', 'History'), ('science', 'Science')], max_length=20)),
                ('author', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to='book/')),
                ('publication', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('quantity', models.PositiveBigIntegerField(default=0)),
                ('availability', models.BooleanField(default=True)),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('wishlist', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BorrowedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('return_date', models.DateField(blank=True, null=True)),
                ('fine_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('fine_paid', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
    ]
