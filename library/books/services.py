from django.db.models import Count
from django.template.loader import render_to_string
from django.http import HttpRequest, JsonResponse

from .forms import BookForm
from .models import Book


def save_book_form(request: HttpRequest, form: BookForm, 
                   template_name: str, user_bind: bool = False):
    data = {}
    
    if request.method == 'POST':
        if form.is_valid():
            print('form is valid')
            book = form.save(commit=False)
            cd = form.cleaned_data
            user = request.user.bookuser
            user.current_page = cd['cur_num_pages']
            user.pages_read += cd['cur_num_pages']
            form.save()
            user.save()
            
            if user_bind:
                book.user.add(user)
            data['status'] = True
            books = Book.objects.all()
            books_not_in_collection = books.annotate(num_collections=Count('collections')).filter(num_collections=0)
            data['html_book_list'] = render_to_string('books/js/books_list_js.html',
                                                      context={'books': books_not_in_collection}, request=request)
            data['status'] = True
        else:
            data['status'] = False
    context = {'form': form,}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def render_to_json_response(request: HttpRequest, html_name: str,
                            template_name: str, context: dict) -> JsonResponse:
    html = render_to_string(template_name, context, request)
    return JsonResponse({html_name: html})
