from django.contrib.auth.models import User
from rest_framework import serializers
from books_and_chapters.models import Book, Chapter

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'