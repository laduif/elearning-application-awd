
from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, StatusUpdateForm, ProfileUpdateForm
from .models import User

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def home(request):
    return render(request, 'accounts/home.html')


@login_required
def profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = StatusUpdateForm(request.POST)

        if form.is_valid():
            status_update = form.save(commit=False)
            status_update.user = request.user
            status_update.save()

            return redirect('profile', user_id=request.user.id)

    else:
        form = StatusUpdateForm()

    status_updates = profile_user.status_updates.all().order_by('-created_at')

    return render(
        request,
        'accounts/profile.html',
        {
            'profile_user': profile_user,
            'status_updates': status_updates,
            'form': form,
        }
    )


@login_required
def search(request):
    if request.user.role != 'TEACHER':
        return redirect('home')

    query = request.GET.get('q', '').strip()

    users = User.objects.none()

    if query:
        users = User.objects.filter(username__icontains=query).order_by('username')

    return render(
        request,
        'accounts/search.html',
        {
            'users': users,
            'query': query,
        }
    )

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            return redirect(
                'profile',
                user_id=request.user.id
            )

    else:
        form = ProfileUpdateForm(
            instance=request.user
        )

    return render(
        request,
        'accounts/edit_profile.html',
        {
            'form': form,
        }
    )

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]