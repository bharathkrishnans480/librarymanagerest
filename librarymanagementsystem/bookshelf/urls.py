
from django.urls import path
from rest_framework.authtoken import views as auth_views

from bookshelf import views

app_name = 'bookshelf'

urlpatterns = [
    path('token-auth/', auth_views.obtain_auth_token),


    path('book/add/', views.BookCreateView.as_view()),
    path('book/all/', views.AllBooksView.as_view()),
    path('book/<int:pk>/', views.BookView.as_view()),
    path('book/edit/<int:pk>/', views.BookUpdateView.as_view()),
    path('book/delete/<int:pk>/', views.DeleteBookView.as_view()),
    path('student/add/', views.CreateStudentView.as_view()),
    path('student/all/', views.ListAllStudentsView.as_view()),
    path('student/<int:pk>/', views.StudentView.as_view()),
    path('student/edit/<int:pk>/', views.UpdateStudentView.as_view()),
    path('student/delete/<int:pk>/', views.StudentRemoveView.as_view()),


    path('issue-book/create/', views.CreateBookIssue.as_view()),
    path('issue-book/list/', views.IssueBookListView.as_view()),
    path('issue-book/update/<int:pk>/', views.IssueBookQuantityUpdateView.as_view()),



]