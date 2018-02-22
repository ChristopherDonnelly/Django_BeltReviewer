from __future__ import unicode_literals 
 
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect
from django.utils.html import escape
from django.contrib import messages
from ..users_app.models import User
from .models import Book, Author, Review
 
def index(request): 
    if not 'user_session' in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['user_session'])
        context = {
            'name': user.first_name,
            'books': Book.objects.all(),
            'reviews': Review.objects.all().order_by("-created_at")[:3]
        }
        return render(request, "book_reviews_app/books.html", context) 

def add(request):
    if not 'user_session' in request.session:
        return redirect('/')
    else:
        context = {
            'authors': Author.objects.all()
        }
        return render(request, "book_reviews_app/add.html", context) 

def add_book(request):
    goto = '/books/add/'
    response = Book.objects.book_validator(request.POST, request.session['user_session'])

    if response['status']:
        goto = '/books/{}'.format(response['book'].id)
    else:
        for tag, error in response['errors'].iteritems():
            messages.error(request, error, extra_tags=tag)

    return redirect(goto)

def add_review(request, book_id):
    goto = '/books/{}'.format(book_id)
    response = Book.objects.review_validator(request.POST, book_id, request.session['user_session'])

    if response['status']:
        goto = '/books/{}'.format(book_id)
    else:
        for tag, error in response['errors'].iteritems():
            messages.error(request, error, extra_tags=tag)

    return redirect(goto)

def delete_review(request, book_id, review_id):
    goto = '/books/{}'.format(book_id)

    Review.objects.get(id = review_id).delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def users(request, user_id):
    if not 'user_session' in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = user_id)
        if user:
            context = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'num_reviews': user.reviews.all().count(),
                'books': Book.objects.values('id', 'title').filter(reviews__user_id = user_id).distinct()
            }
            return render(request, "book_reviews_app/display_user.html", context)
        else:
            return redirect('/')

def books(request, book_id):
    if not 'user_session' in request.session:
        return redirect('/')
    else:
        book = Book.objects.filter( id = book_id )
        if book:
            context = {
                'book': book[0],
                'reviews': book[0].reviews.all().order_by('-created_at')
            }
            return render(request, "book_reviews_app/display_book.html", context)
        else:
            return redirect('/')