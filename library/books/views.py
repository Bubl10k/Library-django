import json
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from collection.forms import CollectionSelectForm

from .forms import BookForm
from .models import Book
from .services import render_to_json_response, save_book_form

# Create your views here.
def book_list(request: HttpRequest) -> HttpResponse:
    user = request.user
    books = user.bookuser.books.all()
    books_not_in_collection = books.annotate(num_collections=Count('collections')).filter(num_collections=0)
    total_books = books.count()
    readd_books = books.filter(status=Book.Status.READ).count()
    unread_books = books.filter(status=Book.Status.UNREAD).count()
    context = {
        'books': books_not_in_collection.order_by('-start_date'),
        'readed_books': readd_books,
        'unreaded_books': unread_books,
        'readed_percentage': int((readd_books / total_books) * 100),
        'unreaded_percentage': int((unread_books / total_books) * 100),
    }
    return render(request, 'books/books_list.html', context)


def create_book(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        form = BookForm(request.POST)
    else:
        form = BookForm()
    return save_book_form(request, form, 'books/book_create.html', user_bind=True)


def delete_book(request: HttpRequest, pk: int) -> JsonResponse:
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.delete()
        books = Book.objects.all()
        return render_to_json_response(request,
                                       'html_book_list',
                                       'books/books_list.html',
                                       {'books': books})
    else:
        return render_to_json_response(request, 
                                       'html_confirm', 
                                       'books/confirm_delete.html', 
                                       {'book': book})


@require_POST
def change_status(request: HttpRequest, pk: int) -> JsonResponse:
    book = get_object_or_404(Book, pk=pk)
    status = json.loads(request.body).get('status')
    
    if status == 'R':
        request.user.bookuser.books_read.add(book)
    book.status = status
    book.save()
    return JsonResponse({'status': True})


def update_book(request: HttpRequest, pk: int) -> JsonResponse:
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
    else:
        form = BookForm(instance=book)
    return save_book_form(request, form, 'books/book_update.html')


@require_POST
def book_favorite(request, pk):
    action = request.POST.get('action')
    book = get_object_or_404(Book, pk=pk)
    
    if action:
        print(action)
        if action == 'favorite':
            book.is_favorite = True
        else:
            book.is_favorite = False
        book.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': 'Not found'})


def add_book_from_collection(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = CollectionSelectForm(request.POST)
        if form.is_valid():
            collection = form.cleaned_data['collection']
            collection.books.add(book)
            collection.save()
            return JsonResponse({'status': True})
    form = CollectionSelectForm()
    return render_to_json_response(request, 'html_form', 
                                   'collection/select_collection.html', 
                                   {'form': form,
                                          'book': book})
    