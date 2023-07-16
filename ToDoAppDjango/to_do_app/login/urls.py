from django.urls import path
from .views import TaskList,DetailedList,EditView,UpdateView,DeleteView,LogIn,RegisterUser
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', LogIn.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
    path('register/', RegisterUser.as_view(),name='register'),
    path('', TaskList.as_view(),name='tasks'),
    path('task/<str:pk>/', DetailedList.as_view(),name='task'),
    path('create-view', EditView.as_view(),name='create-view'),
    path('update-view/<str:pk>/', UpdateView.as_view(),name='update-view'),
    path('delete-view/<str:pk>/', DeleteView.as_view(),name='delete-view'),
]
