from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

# Create your views here.




def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		# jika form valid
		if form.is_valid():
			form.save()
			# new_username = form.cleaned_data.get('username')
			messages.success(request, f'Selamat registrasimu berhasil ! Sekarang kamu udah bisa log in :D')
			return redirect('login')
	else:
		# jika tidak, let it blank
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
	if request.method == 'POST' and 'u_update' in request.POST:
		u_form = UserUpdateForm(request.POST,instance=request.user)
		if u_form.is_valid():
			u_form.save()
			messages.success(request, 'Akunmu berhasil diupdate !')
			return redirect('profile')
	elif request.method == 'POST':
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if p_form.is_valid():
			p_form.save()
			messages.success(request, 'Profilmu berhasil diupdate !')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form':u_form,
		'p_form':p_form
	}
	return render(request, 'users/profile.html', context)
