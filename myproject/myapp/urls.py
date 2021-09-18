from django.contrib import auth
from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name="home"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name = "login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name = "logout.html"), name="logout"),

    # Tasks
    path('tasks/delete-many/', views.DeleteMultipleTasks.as_view(), name="task_delete_many"),
    path('tasks/create/', views.TaskCreateView.as_view(), name="task_create"),
    path('tasks/', views.TaskListView.as_view(), name="task_list"),
    path('tasks/<int:task_id>/update/', views.TaskUpdateView.as_view(), name="task_update"),
    path('tasks/<int:task_id>/delete/', views.TaskDeleteView.as_view(), name="task_delete"),
    path('results/', views.SearchView.as_view(), name='search'),

    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'registration/password_reset.html'), name='password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name = 'registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'registration/password_reset_complete.html'), name='password_reset_complete'),
    path('verify/<auth_token>/', views.VerifyView.as_view(), name='verify'),
]