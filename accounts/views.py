from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render


def login_view(request):
    """Formulario de autenticación usando el User de Django."""
    if request.user.is_authenticated:
        return redirect('user_management')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Has iniciado sesión correctamente.')
            return redirect('user_management')
        messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada.')
    return redirect('login')


@login_required
def user_management(request):
    """Página única para listar, crear y eliminar usuarios."""
    users = User.objects.order_by('username')
    creation_form = UserCreationForm()

    if request.method == 'POST' and 'create_user' in request.POST:
        creation_form = UserCreationForm(request.POST)
        if creation_form.is_valid():
            creation_form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('user_management')
        messages.error(request, 'Revisa los datos del nuevo usuario.')

    context = {
        'users': users,
        'creation_form': creation_form,
    }
    return render(request, 'users.html', context)


@login_required
def delete_user(request):
    if request.method != 'POST':
        return redirect('user_management')

    user_id = request.POST.get('user_id')
    user_to_delete = get_object_or_404(User, pk=user_id)

    if user_to_delete == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario mientras está la sesión iniciada.')
    else:
        user_to_delete.delete()
        messages.success(request, 'Usuario eliminado.')

    return redirect('user_management')


@login_required
def credits_view(request):
    return render(request, 'credits.html')
