from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [

    # --- Hauptseite von Portal
    path('',views.index,name='index'),
    path('news/',views.news,name='news'),
    path('main/',views.main,name='main'),
    path('about/',views.about,name='about'),
    path('maintenance/',views.maintenance,name='maintenance'),
    path('putzplan/',views.putzplan,name='putzplan'),
    path('volunteer/',views.volunteer,name='volunteer'),
    path('utility/',views.utility,name='utility'),
    path('change_duty_status/<int:pk>/',views.change_duty_status,name='change_duty_status'),
    path('comments/<int:pk>/',views.comments,name='comments'),
    path('edit_new/<int:new_id>/',views.edit_new,name='edit_new'),
    path('delete_new/<int:new_id>/',views.delete_new,name='delete_new'),
    path('edit_comment/<int:com_id>/',views.edit_comment,name='edit_comment'),
    path('delete_comment/<int:com_id>/',views.delete_comment, name='delete_comment'),


    # --- Hausmasters interface ---
    path('master_list/',views.master_list,name='master_list'),
    path('master_list_arhiv/',views.master_list_arhiv,name='master_list_arhiv'),
    path('complete_request/<int:pk>/',views.complete_request,name='complete_request'),
    path('task_in_progress/',views.task_in_progress,name='task_in_progress'),
    path('in_progress/<int:pk>/',views.in_progress,name='in_progress'),
    path('task_cancel/<int:pk>/',views.task_cancel,name='task_cancel'),
    path('main_for_masters/',views.main_for_masters,name='main_for_masters'),
    path('canceled_tasks/',views.canceled_tasks,name='canceled_tasks'),

]

