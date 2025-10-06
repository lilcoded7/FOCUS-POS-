from django.urls import path
from accounts.views import *


urlpatterns = [
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_out'),
    path('get/user/email/', get_user_email, name='get_user_email'),
    path('reset/password/', reset_password, name='reset_password')

]