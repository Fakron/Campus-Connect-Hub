from django.urls import path
from .views import question_list_view,question_detail_view, reply_comment_view, create_question, update_question, QuestionDeleteView, like_views, get_like_count,get_like_count_comment

urlpatterns = [
    path('', question_list_view, name="Questionlist"),
    path('questions/<int:pk>/',question_detail_view,name="Questiondetail"),
    path('reply_comment/<int:comment_id>/', reply_comment_view, name='reply_comment'),
    
    path('question/new',create_question,name="create_question"),
    
    path('question/<int:pk>/update',update_question,name="Questionupdate"),
    path('question/<int:pk>/delete',QuestionDeleteView.as_view(),name="Questiondelete"),
    
    # path('comment/<int:pk>/update/', QuestionDetailView.as_view(update_comment=True), name='update_comment'),
    # path('comment/<int:pk>/delete/', QuestionDetailView.as_view(delete_comment=True), name='delete_comment'),
    
    path('like/<int:pk>',like_views,name="like_post"),
    path('get_like_count/<int:pk>/', get_like_count, name='get_like_count'),
    
    
    path('get_like_count_comment/<int:pk>/', get_like_count_comment, name='get_like_count_comment'),

]
