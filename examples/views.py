from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import viewsets, permissions, filters, mixins, generics, status

from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)

from .forms import (
    BookModelForm,
    Bookform,
    CustomUserCreationForm,
    CustomAuthenticationForm,
    BookFilterForm
)
from .models import Book
from django.shortcuts import render,get_object_or_404,redirect
from rest_framework import viewsets
from .serializers import BookSerializer


class BooksListViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    ordering_fields = ('id', 'title','author')
    search_fields = ordering_fields

class Index(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'type' in self.request.GET:
            qs = qs.filter(book_type=int(self.request.GET['type']))
        return qs


class BookCreateView(BSModalCreateView):
    template_name = 'examples/create_book.html'
    form_class = BookModelForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')


class BookUpdateView(BSModalUpdateView):
    model = Book
    template_name = 'examples/update_book.html'
    form_class = BookModelForm
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('index')


class BookReadView(BSModalReadView):
    model = Book
    template_name = 'examples/read_book.html'


class BookDeleteView(BSModalDeleteView):
    model = Book
    template_name = 'examples/delete_book.html'
    success_message = 'Success: Book was deleted.'
    success_url = reverse_lazy('index')

def books(request):
    data = dict()
    if request.method == 'GET':
        books = Book.objects.all()
        data['table'] = render_to_string(
            '_books_table.html',
            {'books': books},
            request=request
        )
        return JsonResponse(data)


def multiple_edit(request):
    if request.method == 'POST':
        ids = request.POST.get('ids')
        ids = ids.split(",")
        for id in ids:
            obj = get_object_or_404(Book, pk=id)
            if request.POST.get('title'):
                obj.title = request.POST.get('title')
            if request.POST.get('author'):
                obj.author = request.POST.get('author')
            if request.POST.get('price'):
                obj.price = request.POST.get('price')
            obj.save()
        return redirect('index')
    else:
        form = Bookform()

    context = {'form': form}
    return render(request, 'examples/_modal.html', context)

def multiple_delete(request):
    if request.method == 'POST':
        ids = request.POST.getlist('books_ids[]')
        for id in ids:
            obj = get_object_or_404(Book, pk=id)
            obj.delete()
        return JsonResponse(True, safe=False)
    else:
        return redirect('index')
