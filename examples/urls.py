from django.urls import path



from django.conf.urls import url, include
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register(r'bookslist', views.BooksListViewSet)

urlpatterns = [
    url('^api/', include(router.urls)),
    path('', views.Index.as_view(), name='index'),
    path('create/', views.BookCreateView.as_view(), name='create_book'),
    path('update/<int:pk>', views.BookUpdateView.as_view(), name='update_book'),
    path('read/<int:pk>', views.BookReadView.as_view(), name='read_book'),
    path('delete/<int:pk>', views.BookDeleteView.as_view(), name='delete_book'),
    path('books/', views.books, name='books'),
]











