from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Book, Chapter, BookForm, ChapterForm
from django.contrib import messages
from .summarize import Summarizer
import json

def homepage(request):
    books = Book.objects.all()
    form_error = False
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
        else:
            form_error = True
        context = {
            'books': books,
            'add_book_form': form,
            'form_error': form_error
        }
        return render(request, 'books.html', context)
    else:
        add_book_form = BookForm()
        context = {
            'books': books,
            'add_book_form': add_book_form,
            'form_error': form_error
        }
        return render(request, 'books.html', context)

def get_book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    try:
        chapter = Chapter.objects.filter(book=book).order_by('chapter_number')
    except Chapter.DoesNotExist:
        chapter = None
    if chapter:
        text = ''
        for chap in chapter:
            text += chap.description
        summary = Summarizer(text).get_summary(len(chapter))
    else:
        summary = ''
    books = Book.objects.all()
    add_book_form = BookForm()
    add_chapter_form = ChapterForm(initial={
        'book': book
    })
    context = {
        'books': books,
        'chapters': chapter,
        'book_detail': book,
        'add_book_form': add_book_form,
        'add_chapter_form': add_chapter_form,
        'summary': summary,
    }
    return render(request, 'book_detail.html', context)

def edit_book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.id)
    else:
        form = BookForm(initial={
            'book_name': book.book_name,
            'author_name': book.author_name,
            'book_read_on': book.book_read_on
        }, instance=book)
        return render(request, 'modals/book_detail_edit_modal.html', {'form': form})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('books')

def add_chapter(request):
    form_error = False
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=request.POST.get('pk'))
        form = ChapterForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.book = book
            form.save()
            messages.success(request, 'Chapter added successfully!')
            return redirect('book_detail', pk=book.id)
        else:
            form_error = True
        context = {
            'books': Book.objects.all(),
            'book_detail': book,
            'add_chapter_form': form,
            'form_error': form_error
        }
        return render(request, 'book_detail.html', context)

def edit_chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    if request.method == 'POST':
        chapter = Chapter.objects.get(pk=pk)
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chapter edited!')
            return redirect('book_detail', pk=chapter.book.id)
    else:
        form = ChapterForm(initial={
            'book':chapter.book,
            'chapter_number':chapter.chapter_number,
            'description':chapter.description
        }, instance=chapter)
        return render(request, 'modals/chapter_edit_modal.html', {'form': form})

def delete_chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    chapter.delete()
    messages.success(request, 'Chapter deleted!')
    return redirect('book_detail', pk=chapter.book.id)

def search_book(request):
    if request.is_ajax():
        q = request.GET.get('term')
        books = Book.objects.filter(book_name__icontains=q)[:10]
        results = []
        for book in books:
            book_json = {}
            book_json['id'] = book.id
            book_json['label'] = book.book_name
            book_json['value'] = book.book_name
            results.append(book_json)
        data = json.dumps(results)
    else:
        book_json = {}
        book_json['id'] = 0
        book_json['label'] = None
        book_json['value'] = None
        data = json.dumps(book_json)
    return HttpResponse(data)