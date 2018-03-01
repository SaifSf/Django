from django.contrib import admin
from .models import Author,Genre,Book,BookInstance,Language

class bookInline(admin.TabularInline):
   model = BookInstance
class booksInline(admin.TabularInline):
   model = Book

class BookAdmin(admin.ModelAdmin):
   list_display= ('title', 'author','summary','isbn','language','display_genre')
   search_fields = ('title','title')
   list_filter = ('title','author')
   inlines= [bookInline]


class BookInstanceAdmin(admin.ModelAdmin):
   list_display= ('id', 'book','due_back','borrower','status')
   fields = ('id', 'book')
   search_fields = ('title','id')
   list_filter = ('due_back','status')

class AuthorAdmin(admin.ModelAdmin):
   list_display = ('first_name','last_name','date_of_birth','date_of_death')
   fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
   search_fields = ('title','first_name')
   list_filter = ('date_of_birth','date_of_death')
   inlines = [booksInline]

admin.site.register(Genre)
admin.site.register(Book,BookAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(BookInstance,BookInstanceAdmin)
admin.site.register(Language)

