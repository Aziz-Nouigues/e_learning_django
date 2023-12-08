from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator

validate_alphanumeric = RegexValidator(
    r'^[a-zA-Z0-9]*$',
    'Only alphanumeric characters are allowed.'
)



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='STUDENT'):
        if not email:
            raise ValueError('Users must have an email address')
        
        # Ensure a valid role is always passed or defaulted
        if role not in ['STUDENT', 'TUTOR', 'ADMINISTRATOR']:  # Or your specific roles
            raise ValueError('Invalid role provided')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        # Superuser creation with the default role as 'ADMINISTRATOR'
        return self.create_user(
            email=email,
            username=username,
            password=password,
            role="ADMINISTRATOR",
        )

class CustomUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, validators=[validate_alphanumeric], default='')
    email = models.EmailField(unique=True)
    dateJoined = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=20, default='STUDENT')

    email_confirmed = models.BooleanField(default=False) 

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.role == "ADMINISTRATOR"
    

#tutor_portal***********************************************************************
class Course(models.Model):
    courseId = models.AutoField(primary_key=True)
    img = models.ImageField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    enrollmentCapacity = models.IntegerField()
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Material(models.Model):
    materialId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    uploadDate = models.DateField(auto_now_add=True)
    documentType = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Assignment(models.Model):
    assignmentId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    dueDate = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Submission(models.Model):
    submissionId = models.AutoField(primary_key=True)
    submissionContent = models.TextField()
    submissionDate = models.DateField(auto_now_add=True)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

class Grade(models.Model):
    gradeId = models.AutoField(primary_key=True)
    grade = models.CharField(max_length=10)
    feedback = models.TextField()
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

class InteractionHistory(models.Model):
    INTERACTION_TYPES = (
        ('upload', 'Upload'),
        ('read', 'Read'),
        # Add more interaction types as needed
    )

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interactions')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    interaction_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} {self.interaction_type} {self.material.title}"
    


class ReadingState(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reading_states')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='reading_states')
    read_state = models.CharField(max_length=20)  # e.g., percentage completed
    last_read_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.student.username}'s reading state for {self.material.title}"
    


class WebRTCSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sdp = models.TextField(blank=True, null=True)
    ice_candidates = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReportedIncident(models.Model):
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reported_user = models.ForeignKey(CustomUser, related_name='reported_user', on_delete=models.CASCADE)
    description = models.TextField()
    resolved = models.BooleanField(default=False)