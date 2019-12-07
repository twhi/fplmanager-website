from main.forms import LoginIdForm, LoginCredsForm


def add_login_modal(request):
    return {
        'login_creds_form': LoginCredsForm(),
        'login_id_form': LoginIdForm(),
    }
