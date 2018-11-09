"""spc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include,url
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from usrs import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^$', views.home, name='home'),
    url(r'^reset/$',
    auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
    ),
    name='password_reset'),
    url(
        r'^files/',
        include('db_file_storage.urls')
    ),
    url(
        r'^model_files/',
        include('usrs.urls', namespace='model_files')
    ),
    # url(r'^yourfiles/$',views.fls, name='your_page'),
    # url(r'^fls/$', views.file_view, name='your_page'),
        # ListView.as_view(
        #     queryset=Book.objects.all(),
        #     template_name='files_list.html'
        # ),
        
    # ),
    # url(r'^add/$',views.file_add,name='file_add'),
        # CreateView.as_view(
        #     model=Book,
        #     form_class=BookForm,
        #     template_name='file_form.html',
        #     success_url=reverse_lazy('your_page')
        # ),
        
    # ),
    url(r'^reset/done/$',
    auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
    auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
    # url(r'^$', views.home, name='home'),
]
