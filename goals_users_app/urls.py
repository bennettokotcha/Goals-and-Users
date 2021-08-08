from django.urls import path
from . import views


urlpatterns = [
    path('', views.register_page),
    path('login', views.login_page),
    path('login-user', views.login_process),
    path('register-user', views.register_user),
    path('userdashboard', views.userdashboard_page),
    path('td/goals', views.goals_page),
    path('create-goal', views.create_goal_page),
    path('create-goal/process', views.create_goal_process),
    path('goals/<int:id>/achieved', views.achieve_goal),
    path('edit-goal/<int:id>', views.edit_goal_page),
    path('goals/<int:id>/edit', views.edit_goal),
    path('delete-goal/<int:id>/process', views.delete_goal),
    path('users/posts/<int:id>', views.posts_page),
    path('users/edit/<int:id>', views.user_edit_page),
    path('edit-i/<int:id>/proccess', views.edit_info_proccess),
    path('edit-p/<int:id>/proccess', views.edit_password_proccess),
    path('edit-d/<int:id>/proccess', views.edit_desc_proccess),
    path('add-post/<int:id>', views.add_post_user),
    path('delete-comment/<int:id>', views.delete_comment),
    path('logout', views.logout),
]