from django.urls import path
from . import views
from . import learn_views
from . import robots_views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('subject/<str:subject>/block/<int:block_number>/', views.block_take, name='block_take'),
    path('subject/<str:subject>/block/<int:block_number>/submit/', views.block_submit, name='block_submit'),
    path('subject/<str:subject>/block/<int:block_number>/note/', views.block_note_save, name='block_note'),
    path('question/<int:pk>/edit/', views.question_edit, name='question_edit'),
    
    # Public Learn/SEO routes
    path('learn/', learn_views.learn_subject_list, name='learn_subject_list'),
    path('learn/<str:subject_slug>/', learn_views.learn_subject_detail, name='learn_subject_detail'),
    path('learn/<str:subject_slug>/<str:block_slug>/', learn_views.learn_block_detail, name='learn_block_detail'),
    path('learn/<str:subject_slug>/<str:block_slug>/<int:question_id>/', learn_views.learn_question_detail, name='learn_question_detail'),
    
    # SEO routes
    path('robots.txt', robots_views.robots_txt, name='robots_txt'),
]

