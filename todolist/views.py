from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todolist, Share, Messenger
from .forms import TodolistForm, ShareForm
from .tasks import send_notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import Http404
import datetime


User = get_user_model()

class TodoList(LoginRequiredMixin,ListView):
    model = Todolist

    def get_context_data(self, **kwargs):
        """
                First owner gets only todolists those created by him
                Then owner gets todolists those were shared to him
        """
        context = super(TodoList, self).get_context_data(**kwargs)
        context['selfcreatedones'] = Todolist.objects.filter(author=self.request.user)
        context['sharedones'] = Share.objects.select_related('todoer').select_related('todoes').filter(todoer = self.request.user).all()
        return context


class TodoView(LoginRequiredMixin,DetailView):
    model = Todolist
    """
                Check if user really is owner of todolist or has comment/view permission
    """
    def get_context_data(self, **kwargs):
        context = super(TodoView, self).get_context_data(**kwargs)
        if Todolist.objects.filter(id=self.kwargs.get('pk'),author = self.request.user).exists():
           context['allowcomment'] = 1
        elif Share.objects.select_related('todoer').select_related('todoes').filter(todoes=self.kwargs.get('pk'),todoer=self.request.user).exists():
           share = Share.objects.select_related('todoer').select_related('todoes').filter(todoes=self.kwargs.get('pk'),todoer=self.request.user).last()
           type = share.type
           if type == 1:
               context['allowcomment'] = 1
           else:
               context['allowcomment'] = 0
        else:
           return Http404()
        context['data'] = context
        try:
            room = Todolist.objects.get(id=self.kwargs.get('pk'))
            messages = Messenger.objects.filter(
                todoapp=room,
            )
            context['room'] = room

        except:
            return Http404()
        return context


    def get(self, request, *args, **kwargs):
        if type(self.get_object()).__name__ == 'HttpResponseRedirect':
            return self.get_object()
        else:
            return super(TodoView, self).get(request, *args, **kwargs)

    # def check_user_follow_or_not(self, profile):
    #     if self.request.user in profile.get_followers() or profile in self.request.user.get_followers():
    #         return True
    #     else:
    #         return False


class TodoCreate(LoginRequiredMixin,CreateView):
   model = Todolist
   form_class = TodolistForm
   success_url = reverse_lazy('todo_list')

   def form_valid(self, form):
       super(TodoCreate, self).form_valid(form)
       """
                When user creates task save it to db then send task to celery to run before the end time
       """
       self.object.author = self.request.user
       self.object.save()
       later = self.object.end_date - datetime.timedelta(minutes=10)
       send_notification.apply_async(args=(self.request.user.pk,), eta=later)
       return super(TodoCreate, self).form_valid(form)


class TodoUpdate(LoginRequiredMixin,UpdateView):
   template_name = "todolist/todolist_edit.html"
   form_class = ShareForm
   model = Todolist
   success_url = reverse_lazy('todo_list')

   def get_object(self, queryset = None):
       obj = super(TodoUpdate, self).get_object(queryset)
       if obj.author == self.request.user:
           return obj
       else:
           return Http404()

   def form_valid(self, form):
       """
                Todolist sharing stuff happens here. Checking if user inserted email or username. Find sharing user
                based on that. Then save sharing user, shared todolist and permission type to the db.
       """
       super(TodoUpdate, self).form_valid(form)
       if '@' in form.cleaned_data['todoer']:
           kwargs = {'email': form.cleaned_data['todoer']}
       else:
           kwargs = {'username': form.cleaned_data['todoer']}
       try:
           user = User.objects.get(**kwargs)
           todolist = Todolist.objects.get(id = self.kwargs['pk'])
           sharing = Share()
           sharing.todoes = todolist
           sharing.todoer = user
           sharing.type = form.cleaned_data['type']
           sharing.save()
       except user.DoesNotExist:
           return Http404()

       return super(TodoUpdate, self).form_valid(form)


class TodoDelete(LoginRequiredMixin, DeleteView):
   model = Todolist
   success_url = reverse_lazy('todo_list')

   def get(self, request, *args, **kwargs):
       return self.delete(request, *args, **kwargs)

   def get_object(self, queryset=None):
       obj = super(TodoDelete, self).get_object(queryset)
       if obj.author == self.request.user:
           return obj
       else:
           return Http404()