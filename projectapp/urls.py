from django.conf.urls import url
from projectapp import views
urlpatterns=[
    # API for adding user
    url(r'^adduser$', views.UserSinup.as_view(), name='UserSinup'),
    # API for userlogin
    url(r'^rnpdlogin$',views.Rnpd_Login.as_view(),name='Rnpd_Login'),
    url(r'^rnpduserlist$',views.Rnpduserlist.as_view(),name='Rnpduserlist'),
    url(r'^rnpuploadfile$',views.Rnpduploadfileview.as_view(),name='Rnpduploadfileview'),
    
]
