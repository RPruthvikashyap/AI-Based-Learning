from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('get_script/<int:script_id>/', views.get_script, name='get_script'),
    path('scripts',views.scripts, name='scripts'),
    path('signup', views.signup, name='signup'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('generate_script/', views.generate_script, name='generate_script'),
    path('login/', views.login_user, name='login'),
    path('edit_script/<int:script_id>/', views.edit_script, name='edit_script'),
    path('delete_script/<int:script_id>/', views.delete_script, name='delete_script'),
    path('generate_quiz/', views.generate_quiz, name='generate_quiz'),
    path('get_generated_quiz/', views.get_generated_quiz, name='get_generated_quiz'),
]