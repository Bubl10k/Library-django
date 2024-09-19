import json
import requests
from django.core.cache import cache
from django.template.loader import render_to_string
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render
from django.conf import settings

from books.models import Book
from books.services import render_to_json_response

from .models import Collection
from .forms import BookSearchForm, CollectionCreateForm

# Create your views here.
def collection_list(request: HttpRequest) -> HttpResponse:
    collections = Collection.objects.\
    filter(user=request.user).filter(user__is_active=True)
    form = BookSearchForm()
    return render(request, 'collection/collection_list.html', 
                  {'collections': collections,
                   'form': form})
    

def get_books_from_collection(request: HttpRequest, pk: int) -> HttpResponse:
    data = {}
    collection = get_object_or_404(Collection, pk=pk)
    books = collection.books.all()
    data['collection'] = render_to_string('collection/collection_books.html', {'books': books,
                                                                               'collection': collection}, 
                                                                                request=request)
    return JsonResponse(data)


@require_POST
def search_books(request: HttpRequest) -> JsonResponse:  
    form = BookSearchForm(request.POST)
    
    if form.is_valid():
        title = form.cleaned_data['title']
        response = requests.get(settings.BOOK_API_URL, 
                                params={'q': title, 'key': settings.BOOK_API_KEY})
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({'status': 'Error', 'message': 'Failed to fetch books from the API.'}, status=500)
    return JsonResponse({'status': 'Error', 'message': 'Invalid data'}, status=500)


@require_POST
def add_book(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Bad JSON'})
    
    title = body.get('title')
    author = body.get('author')
    num_pages = body.get('num_pages')
    description = body.get('description')
    
    if not all([title, author, num_pages]):
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    
    book_user = request.user.bookuser
    book = Book.objects.create(
        title=title, 
        author=author,
        num_pages=num_pages,
        cur_num_pages=0,
        description=description,
        status=Book.Status.UNREAD
    )
    
    book.user.add(book_user)
    book_user.current_page = book.cur_num_pages
    book_user.save()
    
    try:
        collection: Collection = Collection.objects.get(pk=pk)
    except Collection.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Collection not found'}, status=404)
    
    if collection.books.filter(id=book.id).exists():
        return JsonResponse({'status': 'error', 'message': 'Book already in collection'}, status=400)
    else:
        collection.books.add(book)
        collection.save()
    return JsonResponse({'status': 'success', 'book_id': book.id})


def delete_book_from_collection(request: HttpRequest, 
                                collection_pk: int, book_pk: int) -> HttpResponse:
    data = {}
    collection = get_object_or_404(Collection, pk=collection_pk)
    book = get_object_or_404(Book, pk=book_pk)
    
    if request.method == 'POST':
        if book in collection.books.all():
            collection.books.remove(book)
            return render_to_json_response(request, 
                                           'html_books_list',
                                           'collection/collection_books.html', 
                                           {'books': collection.books.all(),
                                                        'collection': collection})
        data['error'] = 'Book not in collection'
        return JsonResponse(data, status=400)
    return render_to_json_response(request,
                                   'html_confirm',
                                   'collection/js/confirm_delete_js.html',
                                                {'book': book,
                                                 'collection': collection})


def add_collection(request: HttpRequest) -> JsonResponse:
    form = CollectionCreateForm()
    cache_key = f'collection_list_{request.user.id}'
    collections = cache.get(cache_key)
    if not collections:
        collections = Collection.objects.\
        filter(user=request.user).filter(user__is_active=True)
        cache.set(cache_key, collections)
    
    data = {'collections': collections} if request.method != 'POST' else {}
    
    if request.method == 'POST':
        form = CollectionCreateForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.user = request.user
            collection.save()
            return render_to_json_response(request,
                                           'html_collection_list',
                                           'collection/js/collection_list_js.html',
                                           {'collections': Collection.objects.all()})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=500)
    data['form'] = form
    return render(request, 'collection/manage_collections.html', data)
           

def delete_collection(request: HttpRequest, pk: int) -> JsonResponse:
    collection = get_object_or_404(Collection, pk=pk)
    
    if request.method == 'POST':
        collection.books.all().delete()
        collection.delete()
        return render_to_json_response(request,
                                       'html_collection_list',
                                       'collection/js/collection_list_js.html',
                                       {'collections': Collection.objects.\
                                                                filter(user=request.user).\
                                                                filter(user__is_active=True)})
    return render_to_json_response(request,
                                   'html_form',
                                   'collection/confirm_delete_collection.html',
                                   {'collection': collection})


def update_collection(request: HttpRequest, pk: int) -> JsonResponse:
    collection = get_object_or_404(Collection, pk=pk)
    form = CollectionCreateForm(instance=collection)
    
    if request.method == 'POST':
        form = CollectionCreateForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            return render_to_json_response(request,
                                           'html_collection_list',
                                           'collection/js/collection_list_js.html',
                                           {'collections': Collection.objects.all()})
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=500)
    
    return render_to_json_response(request, 
                                   'html_form',
                                   'collection/collection_form.html',
                                   {'form': form})
