from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.shortcuts import redirect,render
from django.utils.http import urlsafe_base64_decode
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import  authenticate
from .models import CustomUser as User
class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated


from .forms import LoginForm, Register

class LoginAPI(APIView):
    permission_classes = [IsNotAuthenticated]  # Allow unauthenticated access for login

    def post(self, request):
        form = LoginForm(request.data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                user_info = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    # Add more user attributes as needed
                }
                response_data = {
                    'access_token': access_token,
                    'refresh_token': str(refresh),
                    'user_info': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': user.role
                    }
                }
                if user.role == 'STUDENT':
                    return redirect('student:course-list')
                elif user.role == 'TUTOR':
                    return redirect('tutor:course-list-create')
                else:
                    pass

                # If the user has no role or a role not handled, you can provide a default redirect
                return render(request, 'home.html', response_data)
            else:
                return Response({'detail': 'Invalid credentials'}, status=400)
        else:
            return Response({'detail': 'Invalid form data'}, status=400)


    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


class IsTutorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        # Allow access if user is authenticated and is either a Tutor or an Administrator
        return request.user.is_authenticated and (request.user.role == 'TUTOR' or request.user.role == 'ADMINISTRATOR')

class UserDataView(APIView):
    permission_classes = [IsTutorOrAdmin]  # Requires authenticated user to be a Tutor or an Administrator

    def get(self, request):
        #we used request.user so that the informations of the curent user display(the authenticated user(logged in))
        user = request.user 
        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        })




class RegisterAPI(APIView):
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cuser = serializer.save()
        return Response({
            'user_info': {
                'id': cuser.id,
                'username': cuser.username,
                'email': cuser.email,
                'role': cuser.role,
            },
            'access_token': cuser['access'],
            'refresh_token': cuser['refresh'],
        })
    def get(self, request):
        form = Register()
        return render(request, 'register.html', {'form': form})   



class CanConfirmEmail(BasePermission):
    def has_permission(self, request, view):
        # Allow access only for unconfirmed users
        return not request.user.is_authenticated or not request.user.email_confirmed


class EmailConfirmationView(APIView):
    permission_classes = [CanConfirmEmail]  # Allow access for unconfirmed users
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.email_confirmed = True
                user.save()
                messages.success(request, 'Email confirmed successfully!')
            else:
                messages.error(request, 'Invalid token. Please try again.')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, 'Invalid user. Please try again.')

        return redirect('home')


def home_view(request):
    return render(request, 'home.html')

