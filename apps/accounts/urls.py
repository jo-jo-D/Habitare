from django.urls.conf import path
from .views import SignUpView, LoginView, LogoutView, ProtectedView, EditProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='Common user Sign-Up-view'),
    path('login/', LoginView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile'),
    path('protected/', ProtectedView.as_view(), name='protected'),
               ]