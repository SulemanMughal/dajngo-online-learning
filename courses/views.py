from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Course
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.
from braces.views import LoginRequiredMixin, PermissionRequiredMixin

# ? Home View
def index(request):
    template_name= "courses/index.html"
    context = {
    }
    return render(request, template_name, context)


class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('courses:manage_course_list')
    template_name = 'courses/manage/course/form.html'


# class ManageCourseListView(OwnerCourseMixin, ListView):
#     template_name = 'courses/manage/course/list.html'

class CourseCreateView(PermissionRequiredMixin,OwnerCourseEditMixin, CreateView):
    # pass
    permission_required = 'courses.add_course'

class CourseUpdateView(PermissionRequiredMixin,OwnerCourseEditMixin, UpdateView):
    # pass
    template_name = 'courses/manage/course/form.html'
    permission_required = 'courses.change_course'

class CourseDeleteView(PermissionRequiredMixin,OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'

class ManageCourseListView(OwnerCourseMixin, ListView):
    model = Course
    template_name = 'courses/manage/course/list.html'
    def get_queryset(self):
        qs = super(ManageCourseListView, self).get_queryset()
        return qs.filter(owner=self.request.user)