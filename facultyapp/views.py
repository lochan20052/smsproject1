from django.shortcuts import render, redirect

# Create your views here.

def FacultyHomePage(request):
    return render(request,'facultyapp/FacultyHomePage.html')
#
# # views.py
# from django.shortcuts import render, get_object_or_404
# from .models import BlogPost
#
# def blog_home(request, slug=None):
#     if slug:
#         # Detail view
#         post = get_object_or_404(BlogPost, slug=slug)
#         return render(request, 'facultyapp/BlogSiteManager.html', {'post': post, 'is_detail': True})
#     else:
#         # List view
#         posts = BlogPost.objects.all()
#         return render(request, 'facultyapp/BlogSiteManager.html', {'posts': posts, 'is_detail': False})

from django.shortcuts import render, redirect, reverse, get_object_or_404

#from DjangoProjects.SMS.adminapp.models import StudentList
from .forms import Task_Form
from .models import Task
def add_blog(request):
    if request.method == "POST":
        form = Task_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facultyapp:add_blog')
    else:
        form = Task_Form()
    tasks = Task.objects.all()
    return render(request, 'facultyapp/BlogSiteManager.html', {'form': form, 'tasks': tasks})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('facultyapp:add_blog')

from .forms import AddCourseForm
def add_course(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facultyapp:FacultyHomePage')
    else:
        form = AddCourseForm()
    return render(request, 'facultyapp/add_course.html', {'form': form})


from .models import AddCourse
from adminapp.models import StudentList

def view_student_list(request):
    course = request.GET.get('course')
    section = request.GET.get('section')
    student_courses = AddCourse.objects.all()
    if course:
        student_courses = student_courses.filter(course=course)
    if section:
        student_courses = student_courses.filter(section=section)
    students = StudentList.objects.filter(id__in=student_courses.values('student_id'))
    course_choices = AddCourse.COURSE_CHOICES
    section_choices = AddCourse.SECTION_CHOICES
    context = {
        'students': students,
        'course_choices': course_choices,
        'section_choices': section_choices,
        'selected_course': course,
        'selected_section': section,
    }
    return render(request, 'facultyapp/students.html', context)
