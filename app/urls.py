from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/',views.signout, name='signout'),
    path('profile/', views.Profile, name='profile'),
    path('post/', views.post, name='post'),
    path('edit/', views.edit, name='edit'),
    path('postlike/<int:id>',views.like, name='postlike'),
    path('comment/<int:id>',views.comment, name='comment'),
    path('postdetails/<int:id>',views.postdetails, name='postdetails'),
    path('index/', views.index, name='index'),
    path('chat', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>', views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
]
