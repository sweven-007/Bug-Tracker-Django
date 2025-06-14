from django.shortcuts import render, redirect
from .models import Admin, User, Developer, Category, Priority, Bug
from django.contrib import messages
from django.db.models import Q

'''
Application's Views here.
All the backend logic for differenet pages are written here
'''


def home(request):
    # checking if already logged-in
    if request.session.has_key('admin') and not request.session.has_key('developer') and not request.session.has_key('user'):
        return redirect('/home_admin/')
    elif request.session.has_key('user') and not request.session.has_key('developer') and not request.session.has_key('admin'):
        return redirect('/home_user/')
    elif request.session.has_key('developer') and not request.session.has_key('user') and not request.session.has_key('admin'):
        return redirect('/home_developer/')

    return render(request, 'main/home.html')


def login(request):
    # checking if already logged-in
    if request.session.has_key('admin') and not request.session.has_key('developer') and not request.session.has_key('user'):
        return redirect('/home_admin/')
    elif request.session.has_key('user') and not request.session.has_key('developer') and not request.session.has_key('admin'):
        return redirect('/home_user/')
    elif request.session.has_key('developer') and not request.session.has_key('user') and not request.session.has_key('admin'):
        return redirect('/home_developer/')

    # fetching the role parameter
    role = request.GET.get('role')
    roles = ['admin', 'user', 'developer']

    # checking if role is not empty or invalid
    if not role or role not in roles:
        return redirect('/')

    # if request method is POST i.e, form submitted
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # if logging attempt is made with admin role
        if role == 'admin':
            if Admin.objects.filter(email=email, password=password).exists():
                request.session['admin'] = email
                return redirect('/home_admin/')
            else:
                messages.error(
                    request, "Username or (and) Password is not valid")
                return redirect('/login/?role=admin')

        # if logging attempt is made with developer role
        if role == 'developer':
            if Developer.objects.filter(email=email, password=password).exists():
                request.session['developer'] = email
                return redirect('/home_developer/')
            else:
                messages.error(
                    request, "Username or (and) Password is not valid")
                return redirect('/login/?role=developer')

        # if logging attempt is made with user role
        if role == 'user':
            if User.objects.filter(email=email, password=password).exists():
                request.session['user'] = email
                return redirect('/home_user/')
            else:
                messages.error(
                    request, "Username or (and) Password is not valid")
                return redirect('/login/?role=user')

    # if request method is other that POST i.e, GET
    data = {
        'role': role
    }
    return render(request, 'main/login.html', data)


def home_admin(request):
    # validating for genuine login
    if request.session.has_key('admin'):
        email = request.session['admin']

        developers = Developer.objects.all()
        bugs = Bug.objects.filter(
            resolved=False, rejected=False, assigned_to=None).all()

        admin_object = Admin.objects.get(email=email)

        data = {
            'email': email,
            'developers': developers,
            'bugs': bugs,
        }
        return render(request, 'main/admin.html', data)

    return redirect('/login/?role=admin')


def home_developer(request):
    # validating for genuine login
    if request.session.has_key('developer'):
        email = request.session['developer']

        developer_object = Developer.objects.get(email=email)
        busgs = Bug.objects.filter(resolved=False, assigned_to=developer_object, rejected=False)

        data = {
            'email': request.session['developer'],
            'bugs': busgs
        }
        return render(request, 'main/developer.html', data)

    return redirect('/login/?role=developer')


def home_user(request):
    # validating for genuine login
    if request.session.has_key('user'):
        email = request.session['user']

        priorities = Priority.objects.all()
        categories = Category.objects.all()

        user_object = User.objects.get(email=email)
        bugs = Bug.objects.filter(raised_by=user_object).order_by('-timestamp')

        data = {
            'email': email,
            'priorities': priorities,
            'categories': categories,
            'bugs': bugs,
        }
        return render(request, 'main/user.html', data)

    return redirect('/login/?role=user')


def report_bug(request):
    # function for reporting a new bug, only called by user
    if request.method == 'POST' and request.session.has_key('user'):
        email = request.session['user']

        name = request.POST['name']
        description = request.POST['description']
        priority = request.POST['priority']
        category = request.POST['category']

        priority = Priority.objects.get(name=priority)
        category = Category.objects.get(name=category)

        user_instance = User.objects.get(email=email)

        new_bug_report = Bug(
            name=name,
            description=description,
            priority=priority,
            category=category,
            raised_by=user_instance
        )
        new_bug_report.save()

        return redirect('/home_user/')

    return redirect('/')


def delete_report(request, id_):
    # function for deleting reported_bug
    if request.session.has_key('user'):
        email = request.session['user']
        if Bug.objects.filter(bug_id=id_).exists():
            report = Bug.objects.get(bug_id=id_)
            if report.raised_by == User.objects.get(email=email):
                report.delete()
                return redirect('/home_user/')

    return redirect('/')


def reopen_report(request, id_):
    # function for reopening reported_bug
    if request.session.has_key('user'):
        email = request.session['user']
        if Bug.objects.filter(bug_id=id_).exists():
            report = Bug.objects.get(bug_id=id_)
            if report.raised_by == User.objects.get(email=email):
                report.resolved = False
                report.assigned_to = None
                report.assigned_by = None
                report.save()
                return redirect('/home_user/')

    return redirect('/')


def assign_report(request):
    if request.method == 'POST' and request.session.has_key('admin'):
        email = request.session['admin']

        admin_instance = Admin.objects.get(email=email)

        id_ = request.POST['id_']
        developer = request.POST['assigned_to']

        developer = Developer.objects.get(email=developer)

        report = Bug.objects.get(bug_id=id_)
        report.assigned_to = developer
        report.assigned_by = admin_instance

        report.save()
        return redirect('/home_admin/')

def reject_report(request, id_):
    print("this")
    if request.session.has_key('developer'):
        print("this")

        email = request.session['developer']
        if Bug.objects.filter(bug_id=id_).exists():
            print("this")

            report = Bug.objects.get(bug_id=id_)
            report.rejected = True
            report.resolved = False
            report.save()
            
    return redirect('/home_user/')

def resolve_report(request, id_):
    if request.session.has_key('developer'):
        email = request.session['developer']
        if Bug.objects.filter(bug_id=id_).exists():
            report = Bug.objects.get(bug_id=id_)
            report.rejected = False
            report.resolved = True
            report.save()
            
    return redirect('/home_user/')

    return redirect('/')

def logout(request):
    try:
        del request.session['user']
    except:
        pass
    try:
        del request.session['developer']
    except:
        pass
    try:
        del request.session['admin']
    except:
        pass
    return redirect('/')
