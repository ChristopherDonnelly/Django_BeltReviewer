# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..users_app.models import User

class BookManager(models.Manager):
    def book_validator(self, postData, user_id):
        book_title = postData['book_title']
        author_id = int(postData['author'])
        add_author = postData['add_author']
        review = postData['review']
        rating = postData['rating']
        user = User.objects.get(id = user_id)

        errors = {}
        response = {
            'status': True
        }

        if len(book_title) < 2:
            errors["book_title"] = "Book title should be more than 2 characters"

        if author_id == 0 and len(add_author) < 2:
            errors["add_author"] = "Author name should be more than 2 characters"
        elif author_id == 0 and len(add_author) >= 2:
            author = add_author
        else:
            author = Author.objects.get(id = author_id)

        if len(review) < 10:
            errors["review"] = "Review should not be less than 10 characters"

        if len(errors) == 0:
            exists = Book.objects.filter(title = book_title)

            if not len(exists):
                if author_id == 0 and len(add_author) >= 2:
                    author = Author.objects.create( name = add_author )
                book = Book.objects.create( title = book_title, author = author )
                review = Review.objects.create( rating = rating, content = review, book = book, user = user )
                response['book'] = book
            else:
                errors["book_title"] = "A Book with {} already exists.".format(book_title)

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        
        return response

    def review_validator(self, postData, book_id, user_id):
        review = postData['review']
        rating = postData['rating']
        book = Book.objects.get(id = book_id)
        user = User.objects.get(id = user_id)

        errors = {}
        response = {
            'status': True
        }

        if len(review) < 10:
            errors["review"] = "Review should not be less than 10 characters"

        if len(errors) == 0:
            review = Review.objects.create( rating = rating, content = review, book = book, user = user )

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        
        return response

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "\n\tID: {}\n\tName: {}\n".format(str(self.id), str(self.name))

    __repr__ = __str__

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name = "books")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = BookManager()

    def __str__(self):
        return "\n\tID: {}\n\tTitle: {}\n\tAuthor: {}\n".format(str(self.id), str(self.title), str(self.author.name))

    __repr__ = __str__

class Review(models.Model):
    rating = models.IntegerField()
    content = models.TextField()
    user = models.ForeignKey(User, related_name = "reviews")
    book = models.ForeignKey(Book, related_name = "reviews")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "\n\tID: {}\n\tReviewer: {}\n\tBook Title: {}\n\tRating: {}\n\tRating Content: {}\n\tPosted On: {}\n".format(str(self.id), str(self.user.first_name), str(self.book.title), str(self.rating), str(self.content), str(self.created_at))

    __repr__ = __str__
