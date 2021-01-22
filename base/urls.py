from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.main, name='main'),
    path('vote/<str:poll_id>', views.voteView, name='vote'),
    path('result/<str:poll_id>', views.resultView, name='result'),
    path('create/', views.createView, name='create'),
    path('login/', views.loginView, name='login'),
    path('signup/', views.signUpView, name='signup'),
    path('logout/', views.logOutView, name='logout'),
    path('delete/<str:poll_id>', views.deletePollView, name='delete'),
    path('edit/<str:poll_id>', views.editPollView, name='edit'),
    path('my/polls/', views.pollUserView, name='userpolls'),
    path('itog/', views.HomeView.as_view(), name='home'),
    path('api/chart/data/', views.ChartData.as_view()),
    path('api/data/', views.get_data, name='api-data'),
    path('resultdata/<str:poll_id>/', views.resultData, name='resultdata'),
]