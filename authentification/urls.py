import statistics
from django.urls import include, path
from ALEMNi import settings
from administrator_dash import admin

import student_portal
from student_portal.views import course_list 
import tutor_portal
from tutor_portal.views import CourseListCreateView
from .views import LoginAPI, RegisterAPI, UserDataView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),   
    path('register/', RegisterAPI.as_view(), name='register'),  
    path('user/', UserDataView.as_view(), name='user'), 
    path('student/', include(('student_portal.urls', 'student_portal'), namespace='student')),
    path('tutor/', include(('tutor_portal.urls', 'tutor_portal'), namespace='tutor')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

