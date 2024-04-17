from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

USERNAME_HELP_TEXT = '''
<span class="form-text text-muted">
    <small>
        No máximo 150 caracteres, letras, números e @/./_/-/_ somente
    </small>
</span> '''

PASSWORD1_HELP_TEXT = '''
<ul class="form-text text-muted small">
    <li>Seu password não pode ser similar a outras informações pessoais</li>
    <li>Seu password precisa conter no mínimo 8 caracteres</li>
    <li>Seu password não pode ser uma senha comum</li>
    <li>Seu password não pode conter somente números</li>
</ul>'''

PASSWORD2_HELP_TEXT = '''
<span class="form-text text-muted">
    <small>
        Para verificação é necessáro digitar o mesmo password
    </small>
</span>'''

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder":"Endereço de Email",
            }
        ),
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder":"Primeiro Nome"
            }
        )
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder":"Sobrenome"
            }
        )
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2"
            )
        
        def __init__(self, *args, **kwargs) -> None:
            super(SignUpForm, self).__init__(*args, **kwargs)
            self.fields["username"].widget.attrs["class"] = "form-control"
            self.fields["username"].widget.attrs["placeholder"] = "Usuário"
            self.fields["username"].label = ""
            self.fields["username"].help_text = USERNAME_HELP_TEXT

            self.fields["password1"].widget.attrs["class"] = "form-control"
            self.fields["password1"].widget.attrs["placeholder"] = "Senha"
            self.fields["password1"].label = ""
            self.fields["password1"].help_text = PASSWORD1_HELP_TEXT

            self.fields["password2"].widget.attrs["class"] = "form-control"
            self.fields["password2"].widget.attrs["placeholder"] = "Confirme sua senha"
            self.fields["password2"].label = ""
            self.fields["password2"].help_text = PASSWORD2_HELP_TEXT