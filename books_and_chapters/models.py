from django.db import models
from django import forms

class Book(models.Model):
    book_name       = models.CharField(max_length=200, unique=True)
    author_name     = models.CharField(max_length=200)
    book_read_on    = models.DateField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_name


class Chapter(models.Model):
    book            = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_number  = models.IntegerField()
    description     = models.TextField()

    def __str__(self):
        return self.book.book_name + ': ' + str(self.chapter_number)

class DateInput(forms.DateInput):
    input_type = 'date'

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'book_read_on': DateInput()
        }

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = '__all__'