from django.conf.urls import url
from django.conf.urls import url, include
from django.urls import path

from boards import views

urlpatterns = [

    # url(r'^$',views.home),

    ######BOOK
    url(r'^index$', views.book_index, name="index"),
    url(r'^([0-9]+)/$', views.book_detail, name='detail'),
    path('book_update/<int:id>/', views.book_update, name='book_update'),
    url(r'^delete/([0-9]+)/', views.supp, name='supp'),
    url(r'^add/$', views.add, name='ajouter'),
    url(r'^search/$', views.book_search, name='book_search'),
    path('^comment/<int:id>/$', views.book_comment, name='book_comment'),

    #################user
    url(r'^sign/$', views.signup, name="signup"),
    url(r'^$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),

    ####"librarain##
    path('^update/<int:id>/$', views.User_update, name='user_update'),
    url(r'^user$', views.user_list, name="user_list"),
    url(r'^user_add$', views.user_add, name="user_add"),
    url(r'^user_search$', views.user_search, name="user_search"),
    path('^user/<int:id>/$', views.user_detail, name='user_detail'),
    path('^user_delete/<int:id>/$', views.user_delete, name='user_delete'),
    url(r'^user_brower/([0-9]+)/$', views.book_borrow, name='user_brower'),
]
