from django import forms
from authentification.models import Course



class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['img', 'title', 'description', 'enrollmentCapacity']

