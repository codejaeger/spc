from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import BookForm
from .models import Book
from django.contrib.auth.decorators import login_required

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
				book.save()
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
		except:
			return redirect('login')
		return render(request, 'usrs/file_add.html', {'form': form})



	    
@login_required
def file_view(request):
	user = request.user.files.all()
	return render(request, 'usrs/file_list.html', {'files': user})
