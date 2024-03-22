from django.urls import path
from . import views
from .views import forums
from .views import user_details
from django.contrib import admin

urlpatterns = [    # Existing URL patterns
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blog/blog.html', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('community/book.html/', views.book, name='book'),
    path('community/chat.html/', views.chat, name='chat'),
    path('community/', views.community, name='community'),
    path('community/dir.html/', views.dir, name='dir'),
    path('community/forums.html/', views.forums, name='forums'),
    path('create_article/', views.create_article, name='create_article'),
    path('blog/create_article.html', views.create_article, name='create_article'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/book.html', views.book, name='book'),
    path('dashboard/tasks.html', views.tasks, name='tasks'),
    path('dashboard/profile.html', views.profile, name='profile'), 
    path('details/', views.details, name='details'), 
    path('faq/', views.faq, name='faq'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/dashboard', views.dashboard, name='dashboard'),
    path('community/testimonies.html/', views.testimonies, name='testimonies'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('forums/', forums, name='forums'),
    path('api/user/details/', user_details, name='user_details'),
    path('therapists/', views.view_all_therapists, name='view_all_therapists'),
    path('save_profile/', views.save_profile, name='save_profile'),
    
]
