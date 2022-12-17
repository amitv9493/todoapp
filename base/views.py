from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Task

from django.contrib.auth.views import LoginView

'''for registering new users import these methods'''

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import FormView

# Create your views here.


class customLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    success_url = reverse_lazy('taskist')

    def get_success_url(self) -> str:
        return reverse_lazy('taskist')


# class RegisterPage(FormView):
#     template_name = 'base/register.html'
#     form_class = UserCreationForm

#     redirect_authenticated_user = True
#     success_url = reverse_lazy('login')

#     def form_valid(self, form):
#         return super().form_valid(form)


class RegisterPage(SuccessMessageMixin, CreateView):
    template_name = 'base/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "base/task_list.html"
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input)

        context['search_input'] = search_input
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "base/task_detail.html"
    context_object_name = 'tasks'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "base/task_form.html"
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('taskist')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    template_name = "base/task_form.html"
    success_url = reverse_lazy('taskist')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "base/task_confirm_delete.html"
    context_object_name = 'task'
    success_url = reverse_lazy('taskist')
