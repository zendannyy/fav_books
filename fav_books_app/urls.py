from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.register),
    path('login', views.login),
    path('books', views.books),
    path('books/create', views.book_create),
    path('books/<int:id>', views.books_info),
    path('favorite/<int:id>', views.favorite),
    path('un_favorite/<int:id>', views.un_favorite),
    path('books/<int:book_id>/edit', views.edit),
    path('destroy/<int:id>', views.destroy),
    # path('books/<int:book.id>/edit', views.books_info),
    path('logout', views.logout),
]
