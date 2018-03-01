from django.db import models

# Create your models here.
from django.db.models import Model

from django.urls import reverse  # Used to generate urls by reversing the URL patterns


class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")
    def __str__(self):
        return self.name


class Language(models.Model):
    """
    Model representing a Language (e.g. English, French, Japanese, etc.)
    """
    name = models.CharField(max_length=200,
                            help_text="Enter a the book's natural language (e.g. English, French, Japanese etc.)")
    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField used because Subject can contain many books. Books can cover many subjects.
    # Subject declared as an object because it has already been defined.
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    image=models.ImageField(upload_to="book_images", default = 'media/sf-extension.png')
    copie=models.IntegerField(max_length=999)
    pdfs=models.FileField(upload_to="pdfs")
    def __str__(self):
        return self.title
    def display_genre(self):
        return [g.name for g in self.genre.all()]


import uuid  # Required for unique book instances
from datetime import date

from django.contrib.auth.models import User  # Required to assign User as a borrower


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Book availability')
    def __str__(self):
        return self.status





class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)
    def __str__(self):
        return  self.first_name +" " +self.last_name


class Comment(models.Model):
    content = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.name



