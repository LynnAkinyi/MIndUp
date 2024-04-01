from django.urls import path
from . import views
from .views import forums
from .views import user_details
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import create_group, create_volunteer, create_chat_group, get_chat_groups, upcoming_appointments, delete_appointment
from django.urls import re_path



urlpatterns = [    # Existing URL patterns
    
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blog/blog.html', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('community/book.html/<int:therapist_id>/', views.book, name='book'),path('community/book.html', views.book, name='book'),
    path('community/chat.html/', views.chat, name='chat'),
    path('community/chat.html', views.chat, name='chat'),
    path('community/book.html/', views.book, name='book'),
    path('community/', views.community, name='community'),
    path('community/dir.html/', views.dir, name='dir'),
    path('community/forums.html/', views.forums, name='forums'),
    path('community/forums.html', views.forums, name='forums'),
    path('create_article/', views.create_article, name='create_article'),
    path('blog/create_article.html', views.create_article, name='create_article'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/book.html/<int:therapist_id>/', views.book, name='book'),
    path('dashboard/book.html', views.book, name='book_without_id'),
    path('dashboard/tasks.html', views.tasks, name='tasks'),
    path('saveTaskData', views.save_task_data),
    path('details/', views.details, name='details'), 
    path('faq/', views.faq, name='faq'),
    path('read/', views.read, name='read'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('community/testimonies.html/', views.testimonies, name='testimonies'),
    path('community/testimonies.html', views.testimonies, name='testimonies'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('forums/', forums, name='forums'),
    path('api/user/details/', user_details, name='user_details'),
    path('therapists/', views.view_all_therapists, name='view_all_therapists'),
    path('therapists/book.html/<int:therapist_id>/', views.book, name='book'), 
    path('therapists/book.html', views.book, name='book_without_id'), 
    path('save_profile/', views.save_profile, name='save_profile'),
    path('articles/', views.article_list, name='article_list'),
    path('delete_article/<int:article_id>/', views.delete_article, name='delete_article'),
    path('delete_testimonial/<int:testimonial_id>/', views.delete_testimonial, name='delete_testimonial'),
    path('groups/', create_group, name='create-group'),
    path('volunteers/', create_volunteer, name='create-volunteer'),
    path('groups_and_members/', views.get_all_groups_and_members, name='groups_and_members'),
    path('groups/get_members/<str:group_name>/', views.get_group_members, name='get_group_members'),
    path('create_chat_group/', create_chat_group, name='create_chat_group'),
    path('get_chat_groups/', get_chat_groups, name='get_chat_groups'),
    path('join_chat_group/', views.join_chat_group, name='join_chat_group'),
    path('therapist/<int:therapist_id>/', views.therapist_detail, name='therapist_detail'),
    path('book/<int:therapist_id>/', views.book, name='book'),
    path('schedule_appointment/<int:therapist_id>/', views.schedule_appointment, name='schedule_appointment'),
    path('delete-appointment/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
    path('upcoming-appointments/', upcoming_appointments, name='upcoming_appointments'),
    path('send_message/', views.send_message, name='send_message'),
    path('get_messages/', views.get_messages, name='get_messages'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

