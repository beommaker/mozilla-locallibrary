from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre


def index(request):

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={
            'num_books':num_books, 
            'num_instances':num_instances, 
            'num_instances_available':num_instances_available, 
            'num_authors':num_authors,
            'num_genres':num_genres}
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


def book_detail_view(request,pk):
    
    try:
        book_id=Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    #book_id=get_object_or_404(Book, pk=pk)

    return render(
        request,
        'book_detail.html',
        context={'book':book_id,}
    )
