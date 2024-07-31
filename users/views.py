from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
def signup(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
        
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})
    

def signin(request):
    # print(request)
    if request.method == 'POST':
        form = SignInForm(request.POST)
        # print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username, password)
            user = authenticate(request, username=username, password=password)
            # print(user)
            if user is not None:
                login(request, user)
                # Redirect to the profile page or any other page after successful login
                return redirect('profile')
            else:
                # Handle invalid credentials case
                form.add_error(None, "Invalid username or password.")
        else:
            # Handle form validation errors
            print(form.errors)
            # print("hello")
    else:
        form = SignInForm()

    return render(request, 'signin.html', {'form': form,})



# def signin(request):
#     # print(request)
#     if request.method == 'POST':
#         form = SignInForm(request.POST)
#         # print(form)

#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         print(f"Username: {username}, Password: {password}")


#         user = authenticate(request, username=username, password=password)
#         print(user)
#         if user is not None:
#             login(request, user)
#             # Redirect to the profile page or any other page after successful login
#             return redirect('profile')
#         # else:
#         #     # Handle invalid credentials case
#         #     form.add_error(None, "Invalid username or password.")
#         # # else:
#         # #     # Handle form validation errors
#         # #     print(form.errors)
#         # #     print("hello")
#     else:
#         form = SignInForm()

#     return render(request, 'signin.html', {'form': form})

@login_required
def profile(request):
    if request.method== 'GET':
        user = request.user
        print(user.first_name)
        if request.method == 'GET':
            return render(request, 'profile.html', {"user":user})
    else:
        return render(request, 'home.html')
    

@login_required
def logout_view(request):
    # print('hello')
    logout(request)
    # print('hello2')
    return redirect('signin')
    # return redirect('/')