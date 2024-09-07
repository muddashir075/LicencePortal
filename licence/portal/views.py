from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm, LicenceForm
from .models import User, Licence_Data
from django.contrib.auth.decorators import login_required
from .decorators import allowed_roles
# Create your views here.

@login_required
def home_view(request):
    return render(request, 'licence_home/home.html')

# Create register_view here.
def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get("username")
            #password = form.cleaned_data.get("password")
            #user_type = form.cleaned_data.get("user_type")
            #user = User.objects.create_user(username=username, password=password)
            #login(request, user)
            return redirect('home')
            '''if user.role == 'admin':
                return redirect('accounts/admin_dashboard.html')
            elif user.role == 'manager':
                return redirect('accounts/manager_dashboard.html')
            else:
                return redirect('accounts/resource_dashboard.html')'''
        else:
            messages.error(request, 'Invalid registration data')
            return redirect('home') 
    else:
        form= UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form':form})

# Create login_view here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            '''if user.role == 'admin':
                return redirect('admin_dashboard.html')
            elif user.role == 'manager':
                return redirect('manager_dashboard.html')
            else:
                return redirect('resource_dashboard.html')'''
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
    else:
        error_message = "Invalid Credentials!"
    return render(request, 'accounts/login.html', {'error_message':error_message})

#Create logout_view here.
def logout_view(request):
    if request.method =="POST":
        logout(request)
        return redirect('login')
    else:
        return redirect('home')

#Create Protected_view here.
'''class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    #'next' - to redirect URL
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'licence_home/user_form.html')
'''

#Create create_user_view
def user_create_view(request):
    if request.method == 'POST':
        form = LicenceForm(request.POST, request.FILES)
        if form.is_valid():
            resourse = form.save(commit=False)
            resourse.user = request.user
            resourse.save()
            return redirect('user_list')
    else:
        form= LicenceForm()
    return render(request, 'licence_home/user_form.html', {'form': form})

# Create user_view here.
def user_view(request):
    users = User.objects.all()
    licence_data = Licence_Data.objects.all()
    Users = []
    for user in users:
        licence_info = licence_data.filter(id=user.id)
        Users.append({'user':user, 'licences': licence_info})
    return render(request, 'licence_home/user_list.html', {'Users':Users})

# Create update_view here.
def update_view(request, user_id):
    user = Licence_Data.objects.get(pk=user_id)
    form=LicenceForm()
    if request.method == 'POST':
        form=LicenceForm(request.POST, request.FILES, instance=user) 
        if form.is_valid():
            form.save()
            return redirect('user_list')
    return render(request, 'licence_home/user_form.html', {'form': form}) 

# Create delete_view here.
def delete_view(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        User.delete()
        return redirect('user_list')
    return render(request, 'licence_home/user_confirm_delete.html', {'user': user})

@allowed_roles(['resourse'])
def resource_dashboard(request):
    resource = User.objects.get(id=request.user.id)
    return render(request, 'dashboard/resource_dashboard.html', {'resource': resource})

@allowed_roles(['manager'])
def manager_dashboard(request):
    resources = User.objects.filter(role='resource')
    return render(request, 'dashboard/manager_dashboard.html', {'resources': resources})

@allowed_roles(['admin'])
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'dashboard/admin_dashboard.html', {'users': users})


'''
@login_required
def home_view(request):
    return render(request, 'dashboard/home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(username=username, password=password)
            #form.save()
            login(request, user)
            #messages.success(request, 'User register successfully')
            if user.role == 'admin':
                return redirect('dashboard/admin_dashboard.html')
            elif user.role == 'manager':
                return redirect('dashboard/manager_dashboard.html')
            else:
                return redirect('dashboard/resource_dashboard.html')
        else:
            messages.error(request, 'Invalid registration data')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not  None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'dashboard/home.html'
            return redirect(next_url)
            messages.success(request, 'Logged in successfully')
            if user.role == 'admin':
                next_url = next_url = request.POST.get('next') or request.GET.get('next') or 'dashboard/admin_dashboard.html'
                return redirect(next_url)
            elif user.role == 'manager':
                return redirect('dashboard/manager_dashboard.html')
            else:
                return redirect('dashboard/resource_dashboard.html')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'accounts/login.html')

def user_create_view(request):
    if request.method == 'POST':
        form = LicenceForm(request.POST, request.FILES)
        if form.is_valid():
            resourse = form.save(commit=False)
            resourse.user = request.user
            resourse.save()
            return redirect('user_list')
    else:
        form= LicenceForm()
    return render(request, 'licence_home/user_form.html', {'form': form})

def logout_view(request):
    if request.method =="POST":
        logout(request)
        return redirect('login')
    else:
        return redirect('home')

def user_view(request):
    Users = Licence_Data.objects.all()
    return render(request, 'licence_home/user_list.html', {'Users':Users})

#@allowed_roles(['resourse'])
def resource_dashboard(request):
    resource = User.objects.get(id=request.user.id)
    return render(request, 'dashboard/resource_dashboard.html', {'resource': resource})

#@allowed_roles(['manager'])
def manager_dashboard(request):
    resources = User.objects.filter(role='resource')
    return render(request, 'dashboard/manager_dashboard.html', {'resources': resources})

#@allowed_roles(['admin'])
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'dashboard/admin_dashboard.html', {'users': users})

def update_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            if user.role == 'admin':
                return redirect('dashboard/admin_dashboard.html')
            elif user.role == 'manager':
                return redirect('dashboard/manager_dashboard.html')
            else:
                return redirect('dashboard/resource_dashboard.html')
        else:
            messages.error(request, 'Invalid update data')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'dashboard/edit_user.html')

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('dashboard/admin_dashboard.html')

def update_resource(request, resource_id):
    resource = User.objects.get(id=resource_id)
    if request.method == 'POST':
        form = ResourceUpdateForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('resource_dashboard')
        else:messages.error(request, 'Invalid update data')
    else:
        form = ResourceUpdateForm(instance=resource)
    return render(request, 'dashboard/edit_resource.html', {'resource': resource, 'form': form})

def update_view(request, id):
    User = Licence_Data.objects.get(id=id)
    form=LicenceForm()
    if request.method == 'POST':
        form=LicenceForm(request.POST, instance=User) 
        if form.is_valid():
            form.save()
            return redirect('user_list')
    return render(request, 'licence_home/user_form.html', {'form': form}) 

# Create delete_view here.
def delete_view(request, id):
    User = Licence_Data.objects.get(id=id)
    if request.method == 'POST':
        User.delete()
        return redirect('user_list')
    return render(request, 'licence_home/user_confirm_delete.html', {'User': User})
'''