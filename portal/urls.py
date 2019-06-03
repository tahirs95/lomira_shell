from api.views import book, signup, Logout
from django.contrib import admin

from core.views import index

from django.urls import path, include
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', index, name="home"),
    path('signup/', index, name="signup"),
    path("book/", book, name="book"),
    path("", index, name="index"),
    # path('signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('login/', LoginView.as_view(template_name='authentication/login.html'), name='login'),
    # path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),

    path('login/', obtain_auth_token, name='api_token_auth'),
    path('signup_auth/', include('rest_auth.registration.urls'), name='signup-auth'),
    path('rest-auth/', include('rest_auth.urls')),
    path('logout/', Logout.as_view(), name='logout'),

    path('password_reset/',
        PasswordResetView.as_view(template_name='authentication/password_reset_form.html',
        email_template_name='authentication/password_reset_email.html',
        subject_template_name='authentication/password_reset_subject.txt'), 
        name='password_reset'),
    path('password_reset/done/',
        PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/done/',
        PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'),
        name='password_reset_complete'),
    
]