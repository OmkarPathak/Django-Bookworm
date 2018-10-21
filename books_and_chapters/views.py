from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Book, Chapter, BookForm, ChapterForm
from django.contrib import messages
from .summarize import Summarizer
import json
from datetime import datetime, timedelta
import pickle, random
import os


def get_random_quote():
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'quotes_dump.pckl')
    with open(file_path, 'rb') as file:
        obj = pickle.load(file)
        quote = random.choice(obj)
        return quote

def homepage(request):
    books = Book.objects.filter(added_by_user=request.user).order_by('book_read_on')
    form_error = False
    last_month = datetime.today() - timedelta(days=30)
    last_month_books_count = Book.objects.filter(
            added_by_user=request.user,
            book_read_on__gt=last_month
        ).count()
    total_chapters = Chapter.objects.filter(book__added_by_user=request.user).count()
    quote = get_random_quote()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.added_by_user = request.user
            form.save()
            form = BookForm()
            messages.success(request, 'Book added successfully!')
        else:
            form_error = True
    else:
        form = BookForm()
    context = {
        'quote': quote,
        'books': books,
        'add_book_form': form,
        'form_error': form_error,
        'last_month_books_count': last_month_books_count,
        'total_chapters': total_chapters,
        'total_books': len(books),
    }
    return render(request, 'books.html', context)

def get_book_details(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if book.added_by_user != request.user:
        messages.error(request, 'You are not authenticated to perform this action')
        return redirect('books')
    try:
        chapter = Chapter.objects.filter(book=book).order_by('chapter_number')
    except Chapter.DoesNotExist:
        chapter = None
    if chapter:
        text = ''
        for chap in chapter:
            text += chap.description
        summarizer = Summarizer(text)
        summary = summarizer.get_summary(int(summarizer.get_lenth() * 0.4))
    else:
        summary = ''
    books = Book.objects.filter(added_by_user=request.user).order_by('book_read_on')
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
    if book.added_by_user != request.user:
        messages.error(request, 'You are not authenticated to perform this action')
        return redirect('books')
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', slug=book.slug)
    else:
        form = BookForm(initial={
            'book_name': book.book_name,
            'author_name': book.author_name,
            'book_read_on': book.book_read_on
        }, instance=book)
        return render(request, 'modals/book_detail_edit_modal.html', {'form': form})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.added_by_user != request.user:
        messages.error(request, 'You are not authenticated to perform this action')
        return redirect('books')
    book.delete()
    return redirect('books')

def add_chapter(request):
    form_error = False
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=request.POST.get('pk'))
        if book.added_by_user != request.user:
            messages.error(request, 'You are not authenticated to perform this action')
            return redirect('books')
        form = ChapterForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.book = book
            form.save()
            messages.success(request, 'Chapter added successfully!')
            return redirect('book_detail', slug=book.slug)
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
    if chapter.book.added_by_user != request.user:
        messages.error(request, 'You are not authenticated to perform this action')
        return redirect('books')
    if request.method == 'POST':
        chapter = Chapter.objects.get(pk=pk)
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chapter edited!')
            return redirect('book_detail', slug=chapter.book.slug)
    else:
        form = ChapterForm(initial={
            'book':chapter.book,
            'chapter_number':chapter.chapter_number,
            'description':chapter.description
        }, instance=chapter)
        return render(request, 'modals/chapter_edit_modal.html', {'form': form})

def delete_chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    if chapter.book.added_by_user != request.user:
        messages.error(request, 'You are not authenticated to perform this action')
        return redirect('books')
    chapter.delete()
    messages.success(request, 'Chapter deleted!')
    return redirect('book_detail', slug=chapter.book.slug)

def search_book(request):
    if request.is_ajax():
        q = request.GET.get('term')
        books = Book.objects.filter(
                book_name__icontains=q,
                added_by_user=request.user
            )[:10]
        results = []
        for book in books:
            book_json = {}
            book_json['slug'] = book.slug
            book_json['label'] = book.book_name
            book_json['value'] = book.book_name
            results.append(book_json)
        data = json.dumps(results)
    else:
        book_json = {}
        book_json['slug'] = None
        book_json['label'] = None
        book_json['value'] = None
        data = json.dumps(book_json)
    return HttpResponse(data)