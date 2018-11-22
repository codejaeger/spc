from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import BookForm
from .models import Book , BookIndex
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import hashlib
from functools import partial
from django.db import transaction , IntegrityError
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
@transaction.non_atomic_requests
def file_add(request):
	if request.user.is_authenticated:
		user = request.user
		if request.method == 'POST':
			if not 'check1' in request.POST:
				form = BookForm(request.POST,request.FILES)			
				if form.is_valid():
					try:
						with transaction.atomic():
							key = form.cleaned_data.get('encpt_key')
							scm = form.cleaned_data.get('en_schm')
							shr = form.cleaned_data.get('sharing')
							ls=str(shr).split()
							# if 'md5so' in request.POST():
							# 	book.md5so=request.POST['md5so']
							# else:
							# 	book.md5so=0
							# if 'md5s' in request.POST():
							# 	book.key=request.POST['md5s']
							# else:
							# 	book.key=0
							book = form.save(commit=False)
							book.ownr = user
							# book.it(key,scm)
							f=book.save()
							for el in ls:
								if User.objects.filter(username=el):
									# raise ValidationError("hi")
									ss=User.objects.get(username=el)
									# raise ValidationError(ss.username)
									book.sharedwith.add(ss)
									book.save()
							
					except IntegrityError:
						raise forms.ValidationError("Ongoing sunc in some other client.")
					if f:
						return redirect('model_files:your_page')
					else:
						sd=Book.objects.get(name=book.name,ownr=book.ownr)
						return redirect(sd.get_absolute_url())
				else:
					# raise ValidationError(form.errors)
					return redirect('model_files:your_page')
			else:
				form = BookForm(request.POST,request.FILES)			
				if form.is_valid():
					try:
						with transaction.atomic():
							# shr = request.POST['sharing']
							# ls = str(shr).split()
							book = form.save(commit=False)
							book.md5so=request.POST['md5so']
							book.md5se=request.POST['md5se']
							book.ownr = user
							f=book.save()
					except IntegrityError:
						raise forms.ValidationError("Ongoing sunc in some other client.")
					if f:
						return redirect('model_files:your_page')
					else:
						sd=Book.objects.get(name=book.name,ownr=book.ownr)
						return redirect(sd.get_absolute_url())
				else:
					# raise ValidationError(form.errors)
					return redirect('model_files:your_page')
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
	dfg = Book.objects.filter(sharedwith=request.user)
	user = request.user.files.all()
	for fl in dfg:
		if request.user.files.filter(name=fl.name):
			fl.name=fl.name+"(sharedfile)owner-"+fl.ownr.username
			fl.save()
	al = user | dfg
	# fls = user.order_by('created_at').first()
	# for fls in user:
	# 	i=fls.book_pk;
	# 	sd=Book.objects.get(book_pk=i)
	# 	if not sd.md5s:
	# 		bks=BookIndex.objects.get(book_index_pk=i)
	# 		# bks="asdasd"
	# 		sd.md5s=hashlib.md5((bks.bytes).encode()).hexdigest()
	# 		sd.save()
	return render(request, 'usrs/file_list.html', {'files': al})


# def md5sum(filename):
#     with open(filename, mode='rb') as f:
#         d = hashlib.md5()
#         for buf in iter(partial(f.read, 128), b''):
#             d.update(buf)
#     return d.hexdigest()