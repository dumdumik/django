from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    search_word =  request.GET.get('search_word', ' ')
    search_word_lower = search_word.lower()

    if search_word:
        book_count = Book.objects.filter(title__icontains=search_word_lower).count()
    else:
        book_count = 0

    return render (
        request,
        'index.html',
        context=
        {'num_books':num_books,'num_instances':num_instances, 'num_instances_available':num_instances_available,'num_authors':num_authors, 'search_word':search_word, 'book_count':book_count},
    )

