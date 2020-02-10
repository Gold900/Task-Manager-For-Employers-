from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse


class EmployerTaskView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'work/employer_task_view.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(sender=self.request.user.profile).order_by('-date')


class EmployeeTaskView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'work/employee_task_view.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(reciever=self.request.user.profile).order_by('-date')


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'sender_file', 'deadline', 'reciever']

    def form_valid(self, form):
        form.instance.sender = self.request.user.profile
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.profile.office_tag == 2:
            return True
        return False


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'sender_file', 'deadline']

    def form_valid(self, form):
        form.instance.sender = self.request.user.profile
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user.profile == task.sender:
            return True
        return False


class TaskCompleteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['reciever_file']
    template_name = 'work/employee_completetask_view.html'
    context_object_name = 'task'

    def form_valid(self, form):
        form.instance.reciever = self.request.user.profile

        if form.instance.reciever_file:
            form.instance.status = True
        else:
            form.instance.status = False

        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user.profile == task.reciever:
            return True
        return False

    def get_success_url(self):
        return reverse('work-employeetaskview', kwargs={'username': self.request.user.profile})
