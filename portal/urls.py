from . import views
from django.contrib import admin
from django.urls import path, include
urlpatterns=[
    path('',views.home,name='HOME'),
    path('pdfs', views.question_papers_list, name='pdfs.html'),
    path('download/<int:pk>/', views.download_paper, name='download_paper'),
    path('papers/', views.papers_view, name='papers.html'),
    path('get_filtered_papers/', views.get_filtered_papers, name='get_filtered_papers'),
    path('papers/<int:paper_id>/', views.paper_detail, name='paper_detail'),
    path('api/comments/<int:thread_id>/', views.get_comments, name='get_comments'),
    path('api/comments/', views.post_comment, name='post_comment'),
    path('comments/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('api/', include('api.urls')),
]

