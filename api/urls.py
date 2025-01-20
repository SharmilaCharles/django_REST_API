
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employees', views.EmployeeViewset, basename='employee')
router.register('blogs',views.BlogViewSet,basename='blog')

# router will handle both url pattern for pk and non-pk  operations


urlpatterns = [
    path('students/',views.StudentsView),
    path('students/<int:pk>',views.StudentDetailView), # Function based view

    # path('employees/', views.Employees.as_view()), # Class Based View
    # path('employees/<int:pk>',views.EmployeeDetails.as_view()),

    path('', include(router.urls)),

    # path('blogs/', views.BlogView.as_view()),
    # path('comments/',views.CommentView.as_view()),

    # path('blogs/<int:pk>/', views.BlogDetailView.as_view()),
    # path('comments/<int:pk>/',views.CommentDetailView.as_view()),
    

]