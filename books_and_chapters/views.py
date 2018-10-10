from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Chapter, BookForm, ChapterForm
from django.contrib import messages

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
        return render(request, 'base.html', context)
    else:
        add_book_form = BookForm()
        context = {
            'books': books,
            'add_book_form': add_book_form,
            'form_error': form_error
        }
        return render(request, 'base.html', context)

def get_book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    try:
        chapter = Chapter.objects.filter(book=book).order_by('chapter_number')
    except Chapter.DoesNotExist:
        chapter = None
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
        return render(request, 'book_detail_edit_modal.html', {'form': form})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('books')

def add_chapter(request):
    form_error = False
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=request.POST.get('pk'))
        form = ChapterForm(request.POST)
        print(form)
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