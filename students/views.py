from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


@login_required
def home(request):
    query = request.GET.get('q')

    if query:
        students = Student.objects.filter(roll=query)
    else:
        students = Student.objects.all()

    total = students.count()

    passed = sum(1 for s in students if s.status() == "PASS")
    failed = sum(1 for s in students if s.status() == "FAIL")

    pass_percent = round((passed / total) * 100, 2) if total > 0 else 0
    fail_percent = round((failed / total) * 100, 2) if total > 0 else 0

    return render(request, 'index.html', {
        'students': students,
        'passed': passed,
        'failed': failed,
        'pass_percent': pass_percent,
        'fail_percent': fail_percent
    })


@login_required
def add_student(request):
    if request.method == 'POST':
        Student.objects.create(
            roll=request.POST['roll'],
            name=request.POST['name'],
            tamil=request.POST['tamil'],
            english=request.POST['english'],
            maths=request.POST['maths'],
            science=request.POST['science'],
            social=request.POST['social']
        )
        messages.success(request, "Student added successfully!")
        return redirect('/')
    return render(request, 'add.html')


@login_required
def update_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        try:
            student.name = request.POST.get('name')
            student.tamil = int(request.POST.get('tamil', 0))
            student.english = int(request.POST.get('english', 0))
            student.maths = int(request.POST.get('maths', 0))
            student.science = int(request.POST.get('science', 0))
            student.social = int(request.POST.get('social', 0))

            student.save()
            messages.success(request, "Student updated successfully!")
            return redirect('/')

        except ValueError:
            messages.error(request, "Please enter valid numbers for marks.")

    return render(request, 'update.html', {'s': student})


@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect('/')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/login/')