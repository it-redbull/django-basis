from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404


from .decorators import approved_required
from .forms import CustomPasswordChangeForm, EmailLoginForm, RegistrationForm, ProfileForm


class CustomLoginView(LoginView):
    form_class = EmailLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('register_form', RegistrationForm())
        ctx['active_tab'] = 'login'
        return ctx

    def form_valid(self, form):
        response = super().form_valid(form)
        if not self.request.POST.get('remember'):
            self.request.session.set_expiry(0)
        if not self.request.user.is_approved:
            return redirect('accounts:pending')
        return response


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account aangemaakt! Een beheerder moet je account nog goedkeuren.')
            login(request, user, backend='accounts.backends.EmailBackend')
            return redirect('accounts:pending')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/login.html', {
        'form': EmailLoginForm(request),
        'register_form': form,
        'active_tab': 'register',
    })

def login_redirect(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if not request.user.is_approved:
        return redirect('accounts:pending')
    return redirect('accounts:dashboard')


@login_required
def pending(request):
    """Wachtrij-pagina voor ingelogde, nog niet goedgekeurde gebruikers."""
    if request.user.is_approved:
        return redirect('accounts:dashboard')
    return render(request, 'accounts/pending.html')



@login_required
def change_password_view(request):
    """Wachtwoord wijzigen."""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Wachtwoord succesvol gewijzigd!')
            return redirect('accounts:profile')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def profile(request):
    profiel_form = ProfileForm(instance=request.user, prefix='profiel')
    wachtwoord_form = CustomPasswordChangeForm(request.user, prefix='ww')

    if request.method == 'POST':
        if 'opslaan_profiel' in request.POST:
            profiel_form = ProfileForm(request.POST, instance=request.user, prefix='profiel')
            if profiel_form.is_valid():
                profiel_form.save()
                messages.success(request, 'Je gegevens zijn opgeslagen.')
                return redirect('accounts:profile')
        elif 'opslaan_wachtwoord' in request.POST:
            wachtwoord_form = CustomPasswordChangeForm(request.user, request.POST, prefix='ww')
            if wachtwoord_form.is_valid():
                user = wachtwoord_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Je wachtwoord is gewijzigd.')
                return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {
        'profiel_form': profiel_form,
        'wachtwoord_form': wachtwoord_form,
        'form': wachtwoord_form, 
    })


@approved_required
def dashboard_view(request):
    if request.user.account_type != 'partner':
        return redirect('accounts:profile')


    return render(request, "dashboard.html", {
    })