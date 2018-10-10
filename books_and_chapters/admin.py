from django.contrib import admin
from .models import Book, Chapter

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    pass