# students/urls.py
from django.urls import path
from .views import (
    course_list,
    material_list,
    assignment_list,
    grade_list,
    interaction_list,
    submission_list,
)
app_name = 'student_portal'
urlpatterns = [
    path('courses/', course_list, name='course-list'),
    path('material/', material_list, name='material_list'),
    path('assignment/', assignment_list, name='assignment_list'),
    path('grade/', grade_list, name='grade_list'),
    path('interaction/', interaction_list, name='interaction_list'),
    path('submissions/', submission_list, name='submission-list'),
]