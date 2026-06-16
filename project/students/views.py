from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student


def login_view(request):
    # Fix 8: Redirect already-logged-in users away from login page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
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

    # Fix 7: Use property (no parentheses) for status
    passed = sum(1 for s in students if s.status == "PASS")
    failed = sum(1 for s in students if s.status == "FAIL")

    pass_percent = round((passed / total) * 100, 2) if total > 0 else 0
    fail_percent = round((failed / total) * 100, 2) if total > 0 else 0

    return render(request, 'index.html', {
        'students': students,
        'passed': passed,
        'failed': failed,
        'pass_percent': pass_percent,
        'fail_percent': fail_percent,
        'query': query,
    })


def _validate_marks(post_data):
    """Returns error string or None if valid. Fix 3 & 4: mark range validation."""
    subjects = ['tamil', 'english', 'maths', 'science', 'social']
    for subject in subjects:
        val = post_data.get(subject, '').strip()
        if not val or not val.lstrip('-').isdigit():
            return f"Invalid value for {subject.capitalize()}."
        if not (0 <= int(val) <= 100):
            return f"{subject.capitalize()} must be between 0 and 100."
    return None


@login_required
def add_student(request):
    if request.method == 'POST':
        roll = request.POST.get('roll', '').strip()
        name = request.POST.get('name', '').strip()

        if not roll or not name:
            messages.error(request, "Roll number and name are required.")
            return render(request, 'add.html')

        if Student.objects.filter(roll=roll).exists():
            messages.error(request, "Roll number already exists!")
            return render(request, 'add.html')

        # Fix 3: Validate mark ranges server-side
        error = _validate_marks(request.POST)
        if error:
            messages.error(request, error)
            return render(request, 'add.html')

        Student.objects.create(
            roll=roll,
            name=name,
            tamil=int(request.POST.get('tamil')),
            english=int(request.POST.get('english')),
            maths=int(request.POST.get('maths')),
            science=int(request.POST.get('science')),
            social=int(request.POST.get('social')),
        )
        messages.success(request, "Student added successfully!")
        return redirect('home')

    return render(request, 'add.html')


@login_required
def update_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            tamil = request.POST.get('tamil', '').strip()
            english = request.POST.get('english', '').strip()
            maths = request.POST.get('maths', '').strip()
            science = request.POST.get('science', '').strip()
            social = request.POST.get('social', '').strip()

            if not name or not all([tamil, english, maths, science, social]):
                messages.error(request, "All fields are required.")
                return render(request, 'update.html', {'s': student})

            # Fix 4: Validate mark ranges server-side
            error = _validate_marks(request.POST)
            if error:
                messages.error(request, error)
                return render(request, 'update.html', {'s': student})

            student.name = name
            student.tamil = int(tamil)
            student.english = int(english)
            student.maths = int(maths)
            student.science = int(science)
            student.social = int(social)

            student.save()
            messages.success(request, "Student updated successfully!")
            return redirect('home')

        except ValueError:
            messages.error(request, "Please enter valid numbers for marks.")

    return render(request, 'update.html', {'s': student})


@login_required
def delete_student(request, id):
    if request.method != 'POST':
        return redirect('home')
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect('home')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
