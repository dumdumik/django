from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required



# @permission_required('catalog.can_mark_returned')
# @permission_required('catalog.can_edit')


# def my_view(request):
# class MyView(PermissionRequiredMixin, View):
#     permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AuthorListView(generic.ListView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        return context

class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 2

    def author_detail_view(request, pk):
        try:

            author_id = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404("Author does not exist")

        return render (
            request,
            'catalog/author_detail.html',
            context={"author": author_id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['books'] = Book.objects.filter(author=self.object)
        return context




class BookListView(generic.ListView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 2

    def book_detail_view(request, pk):
        try:
            book_id = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Book does not exist")


        return render(
            request,
            'catalog/book_detail.html',
            context={'book':book_id}
        )


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    search_word =  request.GET.get('search_word', '')
    search_word_lower = search_word.lower()

    if search_word:
        book_count = Book.objects.filter(title__icontains=search_word_lower).count()
    else:
        book_count = 0

    return render (
        request,
        'index.html',
        context=
        {'num_books':num_books,'num_instances':num_instances, 'num_instances_available':num_instances_available,
         'num_authors':num_authors, 'search_word':search_word, 'book_count':book_count, 'num_visits':num_visits},
    )

