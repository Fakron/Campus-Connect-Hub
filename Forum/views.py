from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView , CreateView, UpdateView, DeleteView
from .models import Question, Comment, Category
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms import QuestionForm


def like_views(request, pk):
    post = get_object_or_404(Question, id=pk)
    liked = False
    if post.upvote.filter(id=request.user.id).exists():
        post.upvote.remove(request.user)
        liked = False
    else:
        post.upvote.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('Questiondetail', args=[str(pk)]))

def get_like_count(request, pk):
    question = get_object_or_404(Question, id=pk)
    total_likes = question.total_likes()
    return JsonResponse({'total_likes': total_likes})

def get_like_count_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    total_likes = comment.upvote.count()
    return JsonResponse({'total_likes': total_likes})

class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'Forum/forum.html'
    context_object_name = 'questions'
    ordering = ['-date_created']
    paginate_by = 8  # Number of questions per page

    def get_queryset(self):
        queryset = super().get_queryset()
        search_data = self.request.GET.get('search-area') or ""
        if search_data:
            queryset = queryset.filter(title__icontains=search_data)
        return queryset

    def get_questions_by_category(self, category):
        if category:
            return Question.objects.filter(category=category)
        return Question.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.order_by('-date_created')[:5]     
        categories = Category.objects.all()
        selected_category = self.request.GET.get('category')
        questions = self.get_questions_by_category(selected_category)
        context['comments'] = comments
        context['categories'] = categories 
        context['selected_category'] = selected_category
        context['questions'] = questions
        return context


# class QuestionDetailView(LoginRequiredMixin, DetailView):
#     model = Question
#     template_name = 'Forum/questiondetail.html'
#     context_object_name = 'question'

#     def post(self, request, *args, **kwargs):
#         question = self.get_object()
#         content = request.POST.get('content')
#         Comment.objects.create(question=question, user=request.user, content=content)
#         return redirect('Questiondetail', pk=question.pk)
    
#     def get_context_data(self, *args, **kwargs):
#         context = super(QuestionDetailView, self).get_context_data(*args, **kwargs)
#         question = self.get_object()
#         total_likes = question.total_likes()
#         liked = False

#         if question.upvote.filter(id=self.request.user.id).exists():
#             liked = True
        
#         # Count the total number of comments (answers) for the question
#         total_answers = question.comment.count()

#         # Pass the comments along with their upvote count to the template
#         comments = question.comment.all()
#         comments_with_upvotes = []
#         for comment in comments:
#             upvote_count = comment.upvote.count()
#             comments_with_upvotes.append({'comment': comment, 'upvote_count': upvote_count, 'comment_id': comment.id})

#         context['total_likes'] = total_likes
#         context['liked'] = liked
#         context['total_answers'] = total_answers
#         context['comments_with_upvotes'] = comments_with_upvotes
        
#         return context

def question_detail_view(request, pk):
    question = get_object_or_404(Question, pk=pk)
    total_likes = question.total_likes()
    liked = question.upvote.filter(id=request.user.id).exists()
    total_answers = question.comment.count()
    comments = question.comment.all()
    comments_with_upvotes = []

    for comment in comments:
        upvote_count = comment.upvote.count()
        comments_with_upvotes.append({'comment': comment, 'upvote_count': upvote_count, 'comment_id': comment.id})

    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(question=question, user=request.user, content=content)
        return redirect('question_detail', pk=question.pk)

    context = {
        'question': question,
        'total_likes': total_likes,
        'liked': liked,
        'total_answers': total_answers,
        'comments_with_upvotes': comments_with_upvotes,
        'comments': comments  # Pass the comments queryset to the template
    }
    return render(request, 'Forum/questiondetail.html', context)





def reply_comment_view(request, comment_id):
    if request.method == 'POST':
        # Get the parent comment object
        parent_comment = get_object_or_404(Comment, pk=comment_id)
        # Get the content of the reply from the form
        content = request.POST.get('content')
        reply_comment = Comment.objects.create(
            question=parent_comment.question,
            user=request.user,
            content=content,
            parent_comment=parent_comment
        )
        return redirect('Questiondetail', pk=parent_comment.question.pk)
    # Handle other cases or render appropriate response if needed


        
# @login_required
def create_question(request):
    categories = Category.objects.all()
    print(categories)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = QuestionForm()
        
    context = {
        'form': form,
        'categories': categories  # Make sure categories are included in the context
    }
    return render(request, 'Forum/createquestion.html', context=context)


    

class QuestionUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Question
    fields = ['title','content']
    template_name = 'Forum/createquestion.html'

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        else:
            return False
    

class QuestionDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('home')  # Redirect URL after successful deletion

    def get(self, request, *args, **kwargs):
        # Get the question instance to be deleted
        self.object = self.get_object()
        # Perform deletion directly without a confirmation template
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
    
    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        else:
            return False



