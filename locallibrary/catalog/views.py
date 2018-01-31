from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
from .models import Book, Author, BookInstance, Genre


def index(request):

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={
            'num_books':num_books, 
            'num_instances':num_instances, 
            'num_instances_available':num_instances_available, 
            'num_authors':num_authors,
            'num_genres':num_genres,
            'num_visits':num_visits}
    )


class BookListView(generic.ListView):

    model = Book
    paginate_by = 10

    # your own name for the list as a template variable
    context_object_name = 'book_list'
    # # Get 5 books containing the title 'life'
    # queryset = Book.objects.filter(title__icontains='Life'[:5])
    queryset = Book.objects.all()
    # Specify your own template name/location
    template_name = 'book_list.html'


class BookDetailView(generic.DetailView):
    
    model = Book


class AuthorListView(generic.ListView):
    
    model = Author
    context_object_name = 'author_list'
    queryset = Author.objects.all()
    template_name = 'author_list.html'


class AuthorDetailView(generic.DetailView):

    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')