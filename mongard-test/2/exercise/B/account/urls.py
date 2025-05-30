from django.urls import path
from . import views

app_name = 'account'

urlpatterns= [
    path('register/' , views.UserRegisterView.as_view() , name='user_register' ),
    path('login/' , views.UserLoginView.as_view() , name='user_login'),
    path('logout/' , views.UserLogoutView.as_view() , name='user_logout'),
    path('profile/<int:user_id>' , views.UserProfileView.as_view() , name='user_profile'),
    path('follow/<int:user_id>' , views.UserFollowingView.as_view() , name='user_follow'),
    path('unfollow/<int:user_id>' , views.UserUnFollowingView.as_view() , name='user_unfollow'),
    path('reset-password/' , views.PasswordChangeView.as_view() , name='password_change'),
    path('reset-done/' , views.PasswordResetDoneView.as_view() , name='password_reset_done'),
    path('reset-confirm/<uidb64>/<token>/' , views.PasswordResetConfirmView.as_view() , name='password_reset_confirm'),
    path('reset-complete/' , views.PasswordResetCompleteView.as_view() , name='password_reset_complete'),
]