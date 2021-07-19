from django.views import View
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from . import models
from . import forms

# Create your views here.

class BasePerfil(View):
    template_name = 'perfil/criar.html'

    # Este metodo é executado toda vez que entrar na view
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.perfil = None
        
        if self.request.user.is_authenticated:
            self.perfil = models.Perfil.objects.filter(
                usuario=self.request.user
            ).first()

            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user
                ),
                'perfilform': forms.PerfilForm(data=self.request.POST or None)
            }
        else:
            self.contexto = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'perfilform': forms.PerfilForm(data=self.request.POST or None)
            }

        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']

        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        # Se tiver algum erro no formulário
        if not self.userform.is_valid():
            print('INVÁLIDO!')
            return self.renderizar

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        # Usuário logado
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)
    
            usuario.username = username
            
            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

        # Usuário não logado (novo usuário)
        else:
            # Pegar os dados do formulário - criar usuario | Com o False impedimos que salve na base de dados
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        print('VÁLIDO!')

        # Verificar se consegui obter algum perfil do BD
        print(f'OBTIDO PERFIL: {self.perfil}')
        return self.renderizar
class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')

class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')

class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')
