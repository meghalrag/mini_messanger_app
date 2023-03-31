from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'user'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('userhome/',views.userhome,name='userhome'),
    path('add_post/',views.addpost,name='addpost'),
    path('delete_post/',views.deletepost,name='deletepost'),
    path('ajax_get_post/',views.ajax_get_post,name='ajax_get_post'),
    # path('deleteuser/<int:user_id>',views.deletefunc,name='deleteuser'),
    # path('edituser/<int:user_id>',views.editfunc,name='edituser'),
    # path('viewuser/<int:user_id>',views.viewfunc,name='viewuser'),
    # path('viewuser/getajax/',views.getajax,name='getajax'),
    path('logout/',views.logout,name='logout'),

]
