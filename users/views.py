from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View


class LoginView(View):
    template_name = 'users/login.jinja'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('pages:home')
        return render(request, self.template_name,
                      {'meta_title': 'Login — TaxSaver India'})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        return render(request, self.template_name,
                      {'error': 'Invalid credentials. Please try again.',
                       'meta_title': 'Login — TaxSaver India'})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('pages:home')
