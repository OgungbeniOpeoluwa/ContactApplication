from django.urls import path

from . import views
from .views import search

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('addContacts', views.addContacts, name='addContacts'),
    path('view', views.views, name='views'),
    path('search', views.search, name='search'),
    path('searchbyname', views.searchbyname, name='searchbyname'),
    path('delete', views.delete, name='delete'),
    path('deleteAll', views.deletAll, name='deleteAll'),
    path('back', views.back, name='back'),
    path('editContacts', views.editContact, name='editContact'),
    path('blockContact', views.blockContact, name='blockContact'),
    path('unblockContact', views.unblockContact, name='unblockContact')
    # path('search', search.as_view(), name='search')
]
