from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .serializers import BookSerializer, ChapterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from books_and_chapters.models import Book, Chapter

class BookList(APIView):
    '''
        List all books or create a new book
    '''
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetail(APIView):
    '''
        Retrieve, update or delete a book instance
    '''
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChapterList(APIView):
    '''
        List all books or create a new chapter
    '''
    def get(self, request):
        chapters = Chapter.objects.all()
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChapterDetail(APIView):
    '''
        Retrieve, update or delete a chapter instance
    '''
    def get(self, request, pk):
        chapter = get_object_or_404(Chapter, pk=pk)
        serializer = ChapterSerializer(chapter)
        return Response(serializer.data)

    def put(self, request, pk):
        chapter = get_object_or_404(Chapter, pk=pk)
        serializer = ChapterSerializer(chapter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        chapter = get_object_or_404(Chapter, pk=pk)
        chapter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)