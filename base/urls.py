from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("login/", views.customLoginView.as_view(), name = 'login'),
    path("logout/", LogoutView.as_view(next_page = 'login'), name = 'logout'),
    path("register/", views.RegisterPage.as_view(), name="register"),

    path("",views.TaskList.as_view(),name="taskist"),
    path("task/<int:pk>/", views.TaskDetailView.as_view(), name= 'Task'),
    path("task-create/",views.TaskCreateView.as_view(),name="task-create"),
    path("task-update/<int:pk>",views.TaskUpdateView.as_view(),name="task-update"),
    path("task-delete/<int:pk>",views.TaskDeleteView.as_view(),name="task-delete"),




]