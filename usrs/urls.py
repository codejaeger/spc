from .models import Book
from . import views
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from db_file_storage.compat import url, reverse_lazy
from .forms import BookForm
app_name = 'usrs'

urlpatterns = [
    url(r'^fls/$', views.file_view, name='your_page'),
# 	url(
#         r'^fls/$',
#         ListView.as_view(
#              queryset=Book.objects.all(),
# #            queryset=User.objects.first().files.all(),
#             template_name='usrs/file_list.html'
#         ),
#         name='your_page'
#     ),
    # url(
    #     r'^add/$',
    #     CreateView.as_view(
    #         model=Book,
    #         form_class=BookForm,
    #         template_name='usrs/file_add.html',
    #         success_url=reverse_lazy('model_files:your_page')
    #     ),
    #     name='book.add'
    # ),
    url(r'^add/$', views.file_add, name='book.add'),
    url(
        r'^add/edit/(?P<pk>\d+)/$',
        UpdateView.as_view(
            model=Book,
            form_class=BookForm,
            template_name='usrs/file_add.html',
            success_url=reverse_lazy('model_files:your_page')
        ),
        name='book.adedit'
    ),
    url(
        r'^edit/(?P<pk>\d+)/$',
        UpdateView.as_view(
            model=Book,
            form_class=BookForm,
            template_name='usrs/file_add.html',
            success_url=reverse_lazy('model_files:your_page')
        ),
        name='book.edit'
    ),
    url(
        r'^delete/(?P<pk>\d+)/$',
        DeleteView.as_view(
            model=Book,
            success_url=reverse_lazy('model_files:your_page')
        ),
        name='book.delete'
    ),]
               
    # url(r'^add/$', views.file_add, name='book.add'),

    # url(r'^$', views.home, name='home'),

