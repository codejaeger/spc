from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import BookForm
from .models import Book , BookIndex
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import hashlib
from functools import partial
def home(request):
    return render(request, 'home.html')
# @login_required
# def file_add(request):
#     user = User.objects.first()
#     if request.method == 'POST':
#         form = BookForm(request.POST,request.FILES)
#         if form.is_valid():
#             book = form.save(commit=False)
#             book.ownr = user
#             book.save()
#             return redirect('model_files:your_page')
#     else:
#         form = BookForm()
#     return render(request, 'usrs/file_add.html', {'form': form})
def file_add(request):
	if request.user.is_authenticated:
		user = request.user
		if request.method == 'POST':
			form = BookForm(request.POST,request.FILES)
			if form.is_valid():
				book = form.save(commit=False)
				book.ownr = user
				# book.md5s=md5sum(request.FILES)
				f=book.save()
			if f:
				return redirect('model_files:your_page')
			else:
				sd=Book.objects.get(name=book.name,ownr=book.ownr)
				return redirect(sd.get_absolute_url())

		else:
			form = BookForm()
			return render(request, 'usrs/file_add.html', {'form': form})
	else:
		try:
			username=request.POST['username']
			password=request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request,user)
					user = request.user
					if request.method == 'POST':
						form = BookForm(request.POST,request.FILES)
						if form.is_valid():
							book = form.save(commit=False)
							book.ownr = user
							book.save()
							return redirect('model_files:your_page')
						else:
							form = BookForm()
							return render(request, 'usrs/file_add.html', {'form': form})
		except:
			return redirect('login')
		



	    
@login_required
def file_view(request):
	user = request.user.files.all()
	# fls = user.order_by('created_at').first()
	# for fls in user:
	# 	i=fls.book_pk;
	# 	sd=Book.objects.get(book_pk=i)
	# 	if not sd.md5s:
	# 		bks=BookIndex.objects.get(book_index_pk=i)
	# 		# bks="asdasd"
	# 		sd.md5s=hashlib.md5((bks.bytes).encode()).hexdigest()
	# 		sd.save()
	return render(request, 'usrs/file_list.html', {'files': user})


# def md5sum(filename):
#     with open(filename, mode='rb') as f:
#         d = hashlib.md5()
#         for buf in iter(partial(f.read, 128), b''):
#             d.update(buf)
#     return d.hexdigest()