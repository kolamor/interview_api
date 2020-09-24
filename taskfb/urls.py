from django.urls import path
from . import views


app_name = 'taskfb'

urlpatterns = [
    path('question/', views.QuestionListView.as_view(), name='question_list'),
    path('question/<pk>/', views.QuestionDetailView.as_view(),  name='question_detail'),
    path('interview/', views.InterviewListView.as_view(), name='interview_list'),
    path('interview/active/', views.ActiveInterviewListView.as_view(), name='interview_active'),
    path('interview/<pk>/', views.InterviewDetailView.as_view(),  name='interview_detail'),
    path("login/", views.LoginView.as_view(), name="login"),
    # path('user_answer/', views.PassingInterview.as_view(),  name='passing_interview'),
]
