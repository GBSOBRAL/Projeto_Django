from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    """Faz um logout do usuário"""
    logout(request)
    return HttpResponsePermanentRedirect(reverse('index'))

def register(request):
    """Faz registro de um nova usuário"""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Faz login do usuário e o redireciona para a pagina inicial 
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponsePermanentRedirect(reverse('index'))
    
    context = {'form': form}
    return render(request, 'users/register.html', context)