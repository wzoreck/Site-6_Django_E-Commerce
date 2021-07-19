from django.contrib.auth.models import User
from django import forms
from django.forms import widgets
from . import models

class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        # Quais campos vou querer
        fields = '__all__'
        # Excluindo o campo usuario pois nao queremos a opcao de selecionar um usuario no cadastro
        exclude = ('usuario',)

class UserForm(forms.ModelForm):
    # Não é necessário criar os outros campos do fomulário, vai pegar e configurar conforme estiver no Model
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )
    
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação Senha'
    )

    # Assim podemos saber quem está enviando o formulário
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.usuario = usuario

    class Meta:
        model = User
        # Campos a serem exibidos
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'email')

    def clean(self, *args, **kwargs):
        # Pega os dados 'crus' do formulário
        data = self.data
        # Pega os dados limpos do formulário
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        # Usuário vindo do input template
        usuario_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')
        # Vendo se o usuário já está cadastrado na base de dados
        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'A segunda senha precisa ser igual a primeira'
        error_msg_password_short = 'A senha precisa de pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório'

        # Usuários logados: atualização
        if self.usuario:
            if usuario_db:
                if usuario_data != usuario_db.username:
                    validation_error_msgs['username'] = error_msg_user_exists
            
            if email_db:
                if email_data != email_db.email:
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password2'] = error_msg_password_match
                
                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short
                    
                if len(password2_data) < 6:
                    validation_error_msgs['password2'] = error_msg_password_short

        # Usuário não logados: cadastro
        else:
            if usuario_db:
                validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists

            if not password_data:
                validation_error_msgs['password'] = error_msg_required_field
            
            if not password2_data:
                validation_error_msgs['password2'] = error_msg_required_field
            
            if password_data != password2_data:
                validation_error_msgs['password2'] = error_msg_password_match

            if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short
            
            if len(password2_data) < 6:
                    validation_error_msgs['password2'] = error_msg_password_short


        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))