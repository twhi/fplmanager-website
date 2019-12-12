from django import forms
from .utils import OPT_PARAM_CHOICES

class LoginIdForm(forms.Form):
    unique_id = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Unique FPL ID',
            'id': 'login-id-id'
        }
    ))


class LoginCredsForm(forms.Form):
    username = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',  # specify CSS class
            'placeholder': 'FPL Username',  # default text
            'id': 'login-creds-user'
        }
    ))
    password = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-creds-password',
            'type': 'password',
            'name': 'pw',
        }
    ))


class LineupForm(forms.Form):
    parameter = forms.CharField(
        label='Select optimisation parameter',
        widget=forms.Select(
            choices=OPT_PARAM_CHOICES,
            attrs={
                'class': 'form-control',
            }
        ), initial='ep_next')


class WildcardForm(forms.Form):
    max_budget = forms.FloatField(widget=forms.NumberInput(
        attrs={
            'id': 'max-budget',
            'class': 'form-control',
            'placeholder': 'Specify Maximum Budget'
        }
    ), initial=100.0)
    parameter = forms.CharField(label='Select optimisation parameter', widget=forms.Select(
        choices=OPT_PARAM_CHOICES,
        attrs={
            'id': 'opt-param',
            'class': 'form-control',
        }
    ), initial='ep_next')
    include = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'include',
            'placeholder': 'Players to include',
        }
    ), required=False)
    exclude = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'exclude',
            'placeholder': 'Players to include',
        }
    ), required=False)


class TransferForm(forms.Form):
    num_subs = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'id': 'num-subs',
            'class': 'form-control',
            'placeholder': 'Desired number of subs'
        }
    ), initial=1)
    max_budget = forms.FloatField(widget=forms.NumberInput(
        attrs={
            'id': 'max-budget',
            'class': 'form-control',
            'placeholder': 'Specify Maximum Budget'
        }
    ), initial=100.0)
    parameter = forms.CharField(label='Select optimisation parameter', widget=forms.Select(
        choices=OPT_PARAM_CHOICES,
        attrs={
            'id': 'opt-param',
            'class': 'form-control',
        }
    ), initial='ep_next')
    include = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'include',
            'placeholder': 'Players to include',
        }
    ), required=False)
    exclude = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'exclude',
            'placeholder': 'Players to include',
        }
    ), required=False)
