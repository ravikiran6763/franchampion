from django.conf.urls import url
from django.urls import path
from pdfapp import views

urlpatterns = [
    url(r'^generate/',views.pdf_gen,name='pdf_gen'),
    url(r'^sendMail/', views.sendMail,name='sendMail'), 
    path('sendMail/', views.sendMail),
    url(r'^template1/', views.template1,name='template1'), 
    path('template1/', views.template1),
    url(r'^template2/', views.template2,name='template2'), 
    path('template2/', views.template2),
    
]