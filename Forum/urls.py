from django.urls import path
from .views import QuestionListView,question_detail_view, reply_comment_view, create_question, QuestionUpdateView, QuestionDeleteView, like_views, get_like_count,get_like_count_comment

urlpatterns = [
    path('', QuestionListView.as_view(), name="Questionlist"),
    path('questions/<int:pk>/',question_detail_view,name="Questiondetail"),
    path('reply_comment/<int:comment_id>/', reply_comment_view, name='reply_comment'),

    
    
    path('question/new',create_question,name="create_question"),
    
    
    path('question/<int:pk>/update',QuestionUpdateView.as_view(),name="Questionupdate"),
    path('question/<int:pk>/delete',QuestionDeleteView.as_view(),name="Questiondelete"),
    
    # path('comment/<int:pk>/update/', QuestionDetailView.as_view(update_comment=True), name='update_comment'),
    # path('comment/<int:pk>/delete/', QuestionDetailView.as_view(delete_comment=True), name='delete_comment'),
    
    path('like/<int:pk>',like_views,name="like_post"),
    path('get_like_count/<int:pk>/', get_like_count, name='get_like_count'),
    
    
    path('get_like_count_comment/<int:pk>/', get_like_count_comment, name='get_like_count_comment'),

]
