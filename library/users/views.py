from django.core.cache import cache
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response

from books.models import BookUser
from .serializers import ReadingStatsSerializer
from .forms import EditProfileForm, UserRegistrationForm

from .models import Contact, Profile, ReadingStats

# Create your views here.
def profile_list(request: HttpRequest, follow: bool=False) -> HttpResponse:
    profiles = Profile.objects.\
        filter(book_user__user__is_active=True).\
        exclude(book_user=request.user.bookuser)
    if follow:
        profiles = profiles.\
            filter(book_user__in=request.user.bookuser.\
                following.all())
    for profile in profiles:
        profile.book_count = profile.book_user.\
            get_all_books()
    return render(request, 'users/profile/profile_list.html', 
                  {'profiles': profiles,
                   'follow': follow})


def profile_detail(request: HttpRequest, pk: int, other=False) -> HttpResponse:
    if other:
        profile = get_object_or_404(Profile, pk=pk,
                                    book_user__user__is_active=True)
        return render(request, 'users/profile/profile_others.html', {'profile': profile})
    else:
        profile = get_object_or_404(Profile, pk=pk,
            book_user=request.user.bookuser,
            book_user__user__is_active=True)
        return render(request, 'users/profile/profile.html', {'profile': profile})


def profile_edit(request: HttpRequest, pk):
    profile = Profile.objects.get(pk=pk, 
                                  book_user=request.user.bookuser, 
                                  book_user__user__is_active=True)
    if request.method == 'POST':
        form = EditProfileForm(request.POST,
                               request.FILES, 
                               instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', pk=profile.pk)
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'users/profile/profile_edit.html', {'form': form})


@require_POST
def user_follow(request: HttpRequest) -> JsonResponse:
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    
    if user_id and action:
        cache_key = f'bookuser_{user_id}'
        user = cache.get(cache_key)
        
        try:
            if not user:
                user = BookUser.objects.get(id=user_id)
                cache.set(cache_key, user, timeout=60*5)
            if action == 'Follow':
                Contact.objects.get_or_create(
                    user_from=request.user.bookuser,
                    user_to=user
                )
            else:
                Contact.objects.filter(
                    user_from=request.user.bookuser,
                    user_to=user).delete()
            # Cache delete only when change apply
            cache.delete(f'following_{request.user.bookuser.id}')
            return JsonResponse({'status': 'ok'})
        except BookUser.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


def get_favorites(request: HttpRequest, pk: int) -> JsonResponse:
    user = get_object_or_404(BookUser, pk=pk)
    books = request.user.bookuser.books.filter(is_favorite=True, user=user)
    return JsonResponse({'html_favorite': render_to_string('users/js/favorite_list_js.html', 
                                             {'books': books},
                                             request=request) })


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            print('asd')
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'error', 'errors': user_form.errors})
    user_form = UserRegistrationForm()
    return render(request,'registration/registration_form.html',
                  {'form': user_form})

    
@api_view(['GET'])
def reading_stats(request: HttpRequest, pk: int) -> Response:
    user = get_object_or_404(BookUser, pk=pk)
    queryset = ReadingStats.objects.filter(
        profile__book_user=user)
    serializer = ReadingStatsSerializer(queryset, many=True)
    return Response(serializer.data)
