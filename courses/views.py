from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course, Lesson, Enrollment

def is_instructor(user):
    return user.is_authenticated and user.is_instructor

def course_list(request):
    courses = Course.objects.all()
    query = request.GET.get('q')
    if query:
        courses = courses.filter(title__icontains=query)
    category = request.GET.get('category')
    if category:
        courses = courses.filter(category__icontains=category)
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    return render(request, 'courses/course_detail.html', {'course': course, 'lessons': lessons, 'is_enrolled': is_enrolled})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not request.user.is_instructor:
        Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('course_detail', course_id=course.id)

@login_required
def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    # Check enrollment
    if not Enrollment.objects.filter(student=request.user, course=course).exists() and request.user != course.instructor:
        return redirect('course_detail', course_id=course.id)
    
    lessons = list(course.lessons.all().order_by('created_at'))
    current_index = lessons.index(lesson)
    prev_lesson = lessons[current_index - 1] if current_index > 0 else None
    next_lesson = lessons[current_index + 1] if current_index < len(lessons) - 1 else None

    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson, 
        'course': course, 
        'prev_lesson': prev_lesson, 
        'next_lesson': next_lesson
    })

@user_passes_test(is_instructor)
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'courses/instructor_dashboard.html', {'courses': courses})

@user_passes_test(is_instructor)
def create_course(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST.get('price', 0)
        category = request.POST.get('category', 'General')
        Course.objects.create(title=title, description=description, instructor=request.user, price=price, category=category)
        return redirect('instructor_dashboard')
    return render(request, 'courses/create_course.html')

@user_passes_test(is_instructor)
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        course.title = request.POST['title']
        course.description = request.POST['description']
        course.price = request.POST.get('price', 0)
        course.category = request.POST.get('category', 'General')
        course.save()
        return redirect('instructor_dashboard')
    return render(request, 'courses/edit_course.html', {'course': course})

@user_passes_test(is_instructor)
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('instructor_dashboard')
    return render(request, 'courses/delete_course.html', {'course': course})

@user_passes_test(is_instructor)
def upload_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        title = request.POST['title']
        video_file = request.FILES.get('video_file')
        Lesson.objects.create(course=course, title=title, video_file=video_file)
        return redirect('instructor_dashboard')
    return render(request, 'courses/upload_lesson.html', {'course': course})
