from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView

from boards import form
from .form import AddBook, SignUpForm, UserUpdateForm, BookUpdate, CommentForm
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, request
from boards.models import Book, BookInstance, Author, Language, Genre, Comment


# Create your views here.

def home(request):
    text = "<h1>Bonjour sfs!</h1>"
    return HttpResponse(text)


def book_index(request):
    b = Book.objects.all()
    return render(request, 'index.html', {'books': b})


def book_return(request, id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=id)
        try:
            borrowed_book = BookInstance.objects.get(book=book, borrower=request.user)
        except:
            borrowed_book = None
        book.copies += 1
        book.save()
        borrowed_book.delete()
        return redirect('/%s' % (id))

    return redirect('/%s' % (id))


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    group = Group.objects.get(name='Librarian')
    comments = Comment.objects.filter(book=book)
    commentform = CommentForm()

    form = BookUpdate(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('book_detail', kwargs={'id': id}))

    try:
        borrowed_book = BookInstance.objects.get(book=book, borrower=request.user)
    except:
        borrowed_book = None
    if request.method == 'POST':
        book_borrow(request.user, book)
        return redirect('/')

    context = {'book': book, 'group': group, 'borrowed_book': borrowed_book, 'commentform': commentform,
               'bookform': form, 'comments': comments}
    return render(request, 'detail.html', context)


def supp(request, key):
    group = Group.objects.get(name='Librarian')
    bok = Book.objects.get(id=key)
    if group not in request.user.groups.all():
        return redirect('/index')
    else:
        bok.delete()
    return HttpResponseRedirect('/index')


def add(request):
    form = AddBook(request.POST or None, request.FILES or None)
    group = Group.objects.get(name='Librarian')
    if group not in request.user.groups.all():
        return redirect('/index')
    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/index')
    return render(request, 'ajouter.html', {'form': form})


def book_comment(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.comment_author = request.user
            instance.book = book
            instance.save()

            return redirect('/%s' % (book.id))

    return redirect('/%s' % (book.id))


def book_search(request):
    search = request.GET.get('q');
    book = Book.objects.filter(title=search)
    context = {'book': book}
    return render(request, 'book_search.html', context)


def book_update(request, id=None):
    book = Book.objects.get(id=id)
    form = BookUpdate(request.POST, instance=book)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/%s' % (book.id))

    context = {'form': form}
    return render(request, 'book_update.html', context)


#######Partiii Librayy #######
###########********USERRRRRRRRRRRRRRRRR****************#####

def book_borrow(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        if book.copie > 0:
            borrowed_book = BookInstance()
            borrowed_book.book = book
            borrowed_book.borrower.add(request.user)
            borrowed_book.save()
            book.copie -= 1
            book.save()
            return redirect('/%s' % (book.id))

    return redirect('/%s' % (book.id))


###### signup #####
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/index')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


###### login #####
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('index')
            else:
                print("diaabl")
        else:
            print('incorrect')

    return render(request, 'login.html', {'error_message': 'Invalid login'})


###### logout #####
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


## afficher profile#
def profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    user_profile = {'user': user}
    return render(request, 'profile.html', user_profile)


###### list des userr##

def user_list(request):
    group = Group.objects.get(name='Librarian')
    if group not in request.user.groups.all():
        return redirect('/index')
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


##### search user

def user_search(request):
    group = Group.objects.get(name='Librarian')
    search = request.GET.get('u')
    user = User.objects.filter(username=search)
    if group not in request.user.groups.all():
        return redirect('/index')
    context = {'users': user}
    return render(request, 'user_search.html', context)


#####user view##
def user_detail(request, id):
    user = User.objects.get(id=id)
    return render(request, 'user_detail.html', {'user': user})


####### user delete
def user_delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return HttpResponseRedirect('/user')


########update

def User_update(request, id):
    user = User.objects.get(id=id)
    form = UserUpdateForm(request.POST or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            user.username = form.cleaned_data.get('username')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            form.save()
            return redirect('/user/%s' % (user.id))
    context = {'member': user, 'form': form}
    return render(request, 'user_update.html', context)


##### user add

def user_add(request):
    group = Group.objects.get(name='Librarian')
    form = SignUpForm(request.POST)
    if group not in request.user.groups.all():
        return redirect('/index')
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            grp = Group.objects.get(name='user')
            instance.groups.add(grp)
            return redirect('/user')
    context = {'form': form, 'group': group}
    return render(request, 'librarian_add_user.html', context)

######
