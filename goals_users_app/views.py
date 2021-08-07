from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import User, Post, Goal
from django.contrib import messages
import bcrypt

def register_page(request):
    return render(request, 'register.html')

def login_page(request):
    return render(request, 'login.html')

def create_goal_page(request):
    return render(request, 'create_goal.html')

def userdashboard_page(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
            'all_users': User.objects.all(),
        }
    return render(request, 'all_users.html', context) 

def goals_page(request):
    if not 'user_name' in request.session:
        messages.error(request, 'Must be logged-in or registered in order to continue')
        return redirect('/')
    context = {
        'all_goals': Goal.objects.all(),
        'all_users': User.objects.all(),
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'goals.html', context)
    

def user_edit_page(request, id):
    if request.session['user_id'] == id:
        context = {
            'user': User.objects.get(id=id)
        } 
        return render(request, 'edit_profile.html', context)
    return redirect('/dashboard/admin')

def admin_edit_page(request, id):
    user1 = User.objects.get(id=id)
    # print(user1.user_level, user1.first_name)
    users = User.objects.all()    
    if request.session['user_id'] == id or user1.user_level is True:
        context = {
            'user': User.objects.get(id=id)
        }
        return render(request, 'edit_user.html', context)
    return redirect('/dashboard/admin')

def posts_page(request, id):
    show_user = User.objects.get(id=id)
    context = {
        'show_user' : User.objects.get(id=id),
        'show_user_posts' : show_user.posts_made.all(),
        'all_posts' : Post.objects.all(),
        'logged_user' : User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'posts.html', context)

def register_user(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        user = User.objects.filter(email = request.POST['email'])
        if user:
            messages.error(request, 'Email already exist, please register with a different email address!')
            return redirect('/register')
        if len(errors) > 0 :
            for k, v in errors.items():
                messages.error(request, v)#extra_tags=key
            return redirect('/register')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            print(pw_hash)

            user = User.objects.create(
                first_name=request.POST['first_name'], 
                last_name=request.POST['last_name'],
                username=request.POST['username'],
                email=request.POST['email'],
                desc=request.POST['desc'],
                password=pw_hash,
                confirm_pw=request.POST['confirm_pw']
                )
            request.session['user_id'] = user.id
            request.session['user_name']= user.username
            request.session['first_name']= user.first_name
        return redirect('/userdashboard')

def login_process(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0 :
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/login')
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['first_name'] = logged_user.first_name
            request.session['user_name']= logged_user.username
            request.session['user_id'] = logged_user.id
            return redirect('/userdashboard')
        else:
            messages.error(request, 'Invalid email or password')
        return redirect('/login')
    messages.error(request, 'Invalid email or password')   
    return redirect('/login')

def create_goal_process(request):
    if request.method == 'POST':
        errors = Goal.objects.goal_validator(request.POST)
        if len(errors) > 0 :
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/create-goal')
        else:
            num=request.session['user_id']
            this_user=User.objects.get(id=num)
            create_goal = Goal.objects.create(
                dreamer=this_user,
                goal=request.POST['goal'],
            )
            return redirect('/td/goals')
        return redirect ('/td/goals')

def achieve_goal(request, id):
    if request.method=='GET':
        user = User.objects.get(id=request.session['user_id'])
        goal = Goal.objects.get(id=id)
        user.dreams_acheived.add(goal)
        goal.save()
        return redirect('/td/goals')

def edit_info_proccess(request, id):
    if request.method == 'POST':
        this_user = User.objects.get(id=id)
        errors = User.objects.info_edit_validator(request.POST)
        if not request.POST['email'] == this_user.email:
            user = User.objects.filter(email = request.POST['email'])
            if user:
                messages.error(request, 'Email already exist, please register with a different email address!')
                return redirect(f'/users/edit/{id}')
        if len(errors) > 0 :
            for k, v in errors.items():
                messages.error(request, v)#extra_tags=key
            return redirect(f'/users/edit/{id}')
        this_user = User.objects.get(id=id)
        this_user.first_name = request.POST['first_name']
        this_user.last_name = request.POST['last_name']
        this_user.email = request.POST['email']
        this_user.save()
        return redirect('/dashboard/admin')
    return redirect('/')

def edit_password_proccess(request, id):
    if request.method == 'POST':
        this_user = User.objects.get(id=id)
        errors = User.objects.password_edit_validator(request.POST)
        if len(errors) > 0 :
            for k, v in errors.items():
                messages.error(request, v)#extra_tags=key
            return redirect(f'/users/edit/{id}')

        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        this_user.password = pw_hash
        this_user.confirm_pw = request.POST['confirm_pw']
        this_user.save()
        return redirect('/dashboard/admin')
    return redirect('/')

def edit_desc_proccess(request, id):
    if request.method == 'POST':
        this_user = User.objects.get(id=id)
        this_user.desc = request.POST['desc']
        this_user.save()
        return redirect('/dashboard/admin')

def edit_user_info(request, id):
    if request.method == 'POST':
        this_user = User.objects.get(id=id)
        errors = User.objects.info_edit_validator(request.POST)
        if not request.POST['email'] == this_user.email:
            user = User.objects.filter(email = request.POST['email'])
            if user:
                messages.error(request, 'Email already exist, please register with a different email address!')
                return redirect(f'/admin/edit/{id}')
        if len(errors) > 0 :
            for k, v in errors.items():
                messages.error(request, v)#extra_tags=key
            return redirect(f'/admin/edit/{id}')
        this_user = User.objects.get(id=id)
        this_user.first_name =  request.POST['first_name']
        this_user.last_name = request.POST['last_name']
        this_user.user_level = request.POST['user_level']
        this_user.email = request.POST['email']
        this_user.save()
        return redirect('/dashboard/admin')

def edit_user_password(request, id):
    if request.method == 'POST':
        this_user = User.objects.get(id=id)
        errors = User.objects.password_edit_validator(request.POST)
        if len(errors) > 0 :
            for k, v in errors.items():
                messages.error(request, v)#extra_tags=key
            return redirect(f'/admin/edit/{id}')

        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        this_user.password = pw_hash
        this_user.confirm_pw = request.POST['confirm_pw']
        this_user.save()
        return redirect('/dashboard/admin')
    return redirect('/')

def add_post_user(request, id):
    #add a post to user
    if request.method == 'POST':
        show_user = User.objects.get(id=id)
        num = request.session['user_id']
        logged_user = User.objects.get(id = num)
        create_post = Post.objects.create(
            added_to= show_user,
            posted_by= logged_user,
            message=request.POST['message'],
        )
        logged_user.posts_made.add(create_post)
        show_user.added_posts.add(create_post)
        return redirect(f'/users/show/{id}')


def remove_user(request, number):
    if request.method=='GET':
        user = User.objects.get(id=number)
        if request.session['user_id'] == id or user.user_level is True:
            user.delete()
            return redirect('/dashboard/admin')
        return redirect('/dashboard/admin')

def logout(request):
    request.session.flush()
    return redirect('/')
# Create your views here.

# Create your views here.
