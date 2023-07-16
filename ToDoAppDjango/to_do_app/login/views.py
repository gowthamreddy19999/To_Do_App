from typing import Any, Dict
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.views import LoginView
from .models import ToDo
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth import login

# Create your views here.
# def index(reqest):


class LogIn(LoginView):
    template_name = 'login/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterUser(FormView):
    template_name = 'login/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterUser,self).form_valid(form)

class TaskList(LoginRequiredMixin,ListView):
    model = ToDo
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        print(context)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context

class DetailedList(LoginRequiredMixin,DetailView):
    model = ToDo
    context_object_name = 'tasks'
    template_name = 'login/task.html'

class EditView(LoginRequiredMixin,CreateView):
    model = ToDo
    template_name = 'login/Create_view.html'
    fields = ['description','title','completed']
    success_url = reverse_lazy('tasks')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(EditView,self).form_valid(form)


class UpdateView(LoginRequiredMixin,UpdateView):
    model = ToDo
    fields = '__all__'
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin,DeleteView):
    model = ToDo
    context_object_name = 'tasks'
    template_name = 'login/Delete.html'
    success_url = reverse_lazy('tasks')

