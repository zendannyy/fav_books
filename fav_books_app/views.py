from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
	if request == 'POST':
		return redirect('/')
	else:
		return render(request, 'index.html')


def register(request):
	"""registering and grabbing user id registration flow
	based off the model"""
	if request.method == 'POST':
		errors = User.objects.user_validator(request.POST)
		print("after first if")
		if len(errors) > 0:
			print("after first second")
			for key, value in errors.items():
				messages.error(request, value)
			return redirect('/')
		else:
			# Create User
			user = User.objects.create(
				first_name=request.POST['first_name'],
				last_name=request.POST['last_name'],
				email=request.POST['email'],
				password=request.POST['password'])
			request.session['user_id'] = user.id
			request.session['first_name'] = user.first_name
			return redirect('/books')

	# return redirect('/login')


def login(request):
	"""user login check
	password hash check from db and from form
	"""
	if request.method == 'POST':
		errors = User.objects.user_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value)
			return redirect('/')

	if request.method == "POST":
		users_with_email = User.objects.filter(
			email=request.POST['email'])
		# truthy statement, list with items will be true
		if users_with_email:
			logged_in = users_with_email[0]
			if bcrypt.checkpw(request.POST['password'].encode(), logged_in.password.encode()):
				# store session for ind user
				request.session['user_id'] = logged_in.id
				request.session['first_name'] = logged_in.first_name
				return redirect('/books')
			else:
				messages.error(request, "Either Email or password are not correct")

	return redirect('/')


def books(request):
	"""Books page, for each book"""
	if 'user_id' not in request.session:
		return redirect('/')
	else:
		context = {
			'all_books': Book.objects.all(),
			'this_user': User.objects.get(id=request.session['user_id']),
			'liked': User.objects.filter(id=request.session['user_id']).first().books_liked.all()
		}
		return render(request, 'books.html', context)
	# if request.session['user_id']:
	# 	return render(request, 'books_info.html',
	# 				  {"user": Book.objects.get(
	# 					  id=request.session['user_id'])})
	# else:
	# 	return redirect('/')


def book_create(request):
	"""user can create a book"""
	errors = Book.objects.book_validator(request.POST)
	if len(errors) > 0:
		for k, v in errors.items():
			messages.error(request, v)
		return redirect('/')
	else:
		# objects from Book model
		user_id = request.session['user_id']
		book = Book.objects.create(title=request.POST['title'],
								   author=request.POST['author'],
								   uploaded_by=User.objects.get(id=user_id))
		this_user = User.objects.get(id=user_id)
		# return redirect(f'/books_info/{book.id}')
		return redirect(f'/books/{book.id}')


def books_info(request, id):
	"""GET to retrieve book info"""
	this_user = Book.objects.get(id=id).liked_by.all()
	this_book = Book.objects.get(id=id)
	liked_book = Book.objects.get(id=id).liked_by.filter(id=request.session['user_id'])
	# this makes it possible to have li of user and email under Users who like this book
	# as well as book id information for books_info
	context = {
		'this_user': this_user,
		'this_book': this_book,
		'liked_book': liked_book,

	}
	return render(request, "books_info.html", context)


def favorite(request, id):
	"""Ability to favorite ind books"""
	user_id = request.session['user_id']
	book_placeholder = Book.objects.get(id=id)
	this_user = User.objects.get(id=user_id)
	book_placeholder.liked_by.add(this_user)
	return redirect(f'/books/{id}')


def un_favorite(request, id):
	"""Ability to unfavorite a previously favorited item"""
	user_id = request.session['user_id']
	book_placeholder = Book.objects.get(id=id)
	this_user = User.objects.get(id=user_id)
	book_placeholder.liked_by.remove(this_user)
	return redirect(f'/books/{id}')


def edit(request, book_id):
	"""GET request for edit book form
	takes the changes"""
	book = Book.objects.get(id=book_id)
	book.title = request.POST['title']
	book.author = request.POST['author']
	book.save()
	return redirect(f'/books/{book_id}')


def destroy(request, id):
	"""POST for deleting/destroying a book"""
	book = Book.objects.get(id=id)
	book.delete()
	return redirect('/')


def logout(request):
	"""logout session, back to home page"""
	request.session.flush()
	return redirect('/')
