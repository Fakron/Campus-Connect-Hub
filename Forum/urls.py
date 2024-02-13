from django.urls import path
from .views import QuestionListView,QuestionDetailView, QuestionCreateView, QuestionUpdateView, QuestionDeleteView, like_views

urlpatterns = [
    path('', QuestionListView.as_view(), name="Questionlist"),
    path('questions/<int:pk>/',QuestionDetailView.as_view(),name="Questiondetail"),
    path('question/new',QuestionCreateView.as_view(),name="Questioncreate"),
    path('question/<int:pk>/update',QuestionUpdateView.as_view(),name="Questionupdate"),
    path('question/<int:pk>/delete',QuestionDeleteView.as_view(),name="Questiondelete"),
    
    # path('comment/<int:pk>/update/', QuestionDetailView.as_view(update_comment=True), name='update_comment'),
    # path('comment/<int:pk>/delete/', QuestionDetailView.as_view(delete_comment=True), name='delete_comment'),
    
    path('like/<int:pk>',like_views,name="like_post"),
]
