"""django_bookworm.books_and_chapters URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('books/', login_required(views.homepage), name='books'),       # for adding a new book
    path('books/<int:pk>/', login_required(views.get_book_details), name='book_detail'),
    path('books/<int:pk>/delete/', login_required(views.delete_book), name='delete_single_book'),
    path('books/<int:pk>/edit/', login_required(views.edit_book_details), name='book_details_edit'),
    path('chapters/add/', views.add_chapter, name='add_chapter'),
    # path('chapters/<int:pk>/delete/', views.delete_chapter, name='delete_chapter'),
    # path('chapters/<int:pk>/edit/', views.edit_chapter, name='edit_chapter'),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False))
]
