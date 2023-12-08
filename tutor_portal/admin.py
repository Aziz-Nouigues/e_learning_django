from django.contrib import admin

# Register your models here.

from authentification.models import CustomUser
from authentification.models import Course
from authentification.models import Material
from authentification.models import Assignment
admin.site.register(Course)
admin.site.register(CustomUser)
admin.site.register(Material)
admin.site.register(Assignment)
