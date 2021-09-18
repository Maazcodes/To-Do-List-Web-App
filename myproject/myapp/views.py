from myapp.models import MyTasks, Profile
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from myapp.forms import TasksForm, UserRegistrationForm
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
import uuid
from django.http import HttpResponseRedirect
# Create your views here.


class SignupView(SuccessMessageMixin, TemplateView):
    
    success_message = 'Success!! You have created your account'
    success_url = reverse_lazy('home')
    template_name = 'signup.html'
    model = Profile

    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # messages.success(request, f'{username.capitalize()}, you have created your account successfully.')
            username = form.cleaned_data.get('username')
            userobj = User.objects.get(username = username)
            email = userobj.email
            auth_token = str(uuid.uuid4())
            profile_obj = self.model.objects.create(user = userobj, auth_token=auth_token)
            profile_obj.save()
            self.sendemail_after_signup(request, email, auth_token, username, **kwargs)
            return TemplateResponse(self.request, 'send_token.html')

        return TemplateResponse(request, self.template_name, self.get_context_data(form=form))


    def sendemail_after_signup(self,request, email, token, username, **kwargs):
        domain = request.get_host()
        protocol = request.scheme
        subject = 'Email Verification'
        context = self.get_context_data(**kwargs)
        context.update(domain=domain, protocol= protocol, token=token,username=username)
        html_message = render_to_string('email_verification_content.html', context)
        message = strip_tags(html_message) # no need to use strip_tags because html tags are already stripped when we use render_to_string and keyword argument 'html_message' in send_email
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        email = EmailMessage(subject, message, from_email=email_from, to = recipient_list)
        email.send()
        # send_mail(subject, message, email_from, recipient_list, html_message=html_message)


class VerifyView(TemplateView):
    model = Profile

    def get(self, request, auth_token, **kwargs):
        try:
            profile_obj = self.model.objects.filter(auth_token=auth_token).first()
            if profile_obj:
                if profile_obj.is_verified:
                    messages.success(request, "Your account is already verified")
                    return HttpResponseRedirect(reverse('login'))
                profile_obj.is_verified = True
                profile_obj.save()
                messages.success(request, "Your email has been verified. You can now login into your account")
                return redirect('login')
            else:
                return TemplateResponse(self.request, 'error.html') 

        except Exception as e:
            print(e)
            return redirect('home')


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username.capitalize()}, you have successfully created an account")
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', context={'form':form})


def homepage(request):
    return render(request, 'home.html')


class TaskListView(LoginRequiredMixin, ListView):
    """List of all tasks."""

    model = MyTasks
    context_object_name = 'tasks'
    template_name = 'task_list.html'
    paginate_by = 5
    ordering = ['-task_date']
    queryset = MyTasks.objects.all()

    def get_queryset(self):
        user = self.request.user
        return MyTasks.objects.filter(user = user)
        
    # def get_context_data(self, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)
    #     context['tasks'] = MyTasks.user.all()
    #     return context
    # raise_exception = True
    # permission_denied_message = "Permission Denied Message by me"

class TaskCreateView(SuccessMessageMixin, CreateView):
    """View to create new task."""

    model = MyTasks
    context_object_name = 'task'
    template_name = 'task_create.html'
    raise_exception = True
    success_message = 'Task successfully created!'
    # fields = ['task_title', 'task_desc', 'taskDate','taskTime']
    success_url = reverse_lazy('task_list')
    form_class = TasksForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(SuccessMessageMixin, UpdateView):
    """View to edit or update task."""
    model = MyTasks
    context_object_name = 'task'
    raise_exception = True
    # fields = ['task_title', 'task_desc', 'taskDate', 'taskTime']
    success_message = 'Task successfully updated!'
    success_url = reverse_lazy('task_list')
    template_name = 'task_update.html'
    pk_url_kwarg = 'task_id'
    form_class = TasksForm
   

class TaskDeleteView(DeleteView):
    """View to delete a task."""
    model = MyTasks
    raise_exception = True
    context_object_name = 'task'
    success_message = 'Task successfully deleted!'
    success_url = reverse_lazy('task_list')
    template_name = 'task_delete.html'
    pk_url_kwarg = 'task_id'

    def delete(self, request, *args, **kwargs):
        """Override delete method to allow success message to be added."""
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class DeleteMultipleTasks(SuccessMessageMixin, View):
    success_url = reverse_lazy('task_list')
    success_message = 'Task successfully deleted!'

    def post(self, request, *args, **kwargs):
        tasks = self.request.POST.getlist('tasks_delete')
        tasks_to_delete = MyTasks.objects.filter(task_id__in = tasks).delete()
        # if 0 tasks selected, then tasks_to_delete = {0,{}} else if one selected, 
        # tasks_to_delete = {1, {'myapp.MyTasks':1}}
        if tasks_to_delete[0] !=0: # validation if the user clicks on delete button without selecting the task.
            messages.success(self.request, self.success_message)
        else:
            messages.info(self.request, "Please select the task to delete.")
        return redirect(reverse_lazy('task_list'))

class SearchView(ListView):
    model = MyTasks
    context_object_name = 'all_search_results'
    template_name = 'search.html'
    result = None
    def get_queryset(self, *args, **kwargs):
        self.result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = MyTasks.objects.filter( task_title__icontains = query)
            # icontains means it will search the query irrespective of case.
            # It will search the query only from task title.
            self.result = postresult
        else:
            self.result = None
        return self.result

    # Just tried this method, not used anywhere
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = self.result
        return context

