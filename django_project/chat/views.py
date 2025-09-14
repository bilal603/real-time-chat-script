import logging
logger = logging.getLogger(__name__)
def user_list(request):
	from django.contrib.auth.models import User
	users = User.objects.all()
	return render(request, 'chat/user_list.html', {'users': users})
from django.contrib.auth import login, logout
from django.contrib import messages
from django import forms



def logout_view(request):
	logout(request)
	request.session.flush()
	return redirect('signup')
from django.contrib.auth.models import User

from django.shortcuts import render

def chat_page(request):
	if not request.user.is_authenticated:
		return redirect('signup')
	return render(request, 'chat/chat.html')

from .forms import CustomSignupForm
from django.shortcuts import redirect

def signup(request):
	logger.info(f"Signup page accessed by IP: {request.META.get('REMOTE_ADDR')}")
	if request.user.is_authenticated:
		return redirect('chat')

	if request.method == 'POST':
		form = CustomSignupForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			user = User.objects.filter(email=email).first()
			if user:
				logger.info(f"User login: {email} (ID: {user.id})")
				login(request, user)
				request.session['user_name'] = user.first_name
				return redirect('chat')
			else:
				user = User.objects.create_user(
					username=email,
					first_name=form.cleaned_data['name'],
					last_name=form.cleaned_data['last_name'],
					email=email
				)
				logger.info(f"New user registered: {email} (ID: {user.id})")
				login(request, user)
				request.session['user_name'] = user.first_name
				return redirect('chat')
		else:
			form = CustomSignupForm()
	else:
		form = CustomSignupForm()
	return render(request, 'chat/signup.html', {'form': form})


