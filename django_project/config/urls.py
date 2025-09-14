from django.contrib import admin
from django.urls import path

from chat.views import chat_page, signup, logout_view, user_list

urlpatterns = [
    path('', signup, name='signup'),
    path('admin/', admin.site.urls),
    path('chat/', chat_page, name='chat'),
    path('logout/', logout_view, name='logout'),
    path('users/', user_list, name='user_list'),
]
