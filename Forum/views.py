from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView , CreateView, UpdateView, DeleteView

from Community.models import Room
from .models import Question, Comment, Category, Tag
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms import QuestionForm
from django.contrib.auth.decorators import login_required


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

def question_list_view(request):
    queryset = Question.objects.order_by('-date_created')
    search_data = request.GET.get('search-area') or ""
    if search_data:
        queryset = queryset.filter(title__icontains=search_data)

    selected_category = request.GET.get('category')
    if selected_category:
        queryset = queryset.filter(category=selected_category)

    paginator = Paginator(queryset,10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    comments = Comment.objects.order_by('-date_created')[:5]
    categories = Category.objects.all()

    user_rooms = Room.objects.filter(participant=request.user)

    context = {
        'questions': page_obj,
        'comments': comments,
        'categories': categories,
        'selected_category': selected_category,
        'user_rooms': user_rooms,
    }
    return render(request, 'Forum/forum.html', context)

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
        return redirect('Questiondetail', pk=question.pk)

    context = {
        'question': question,
        'total_likes': total_likes,
        'liked': liked,
        'total_answers': total_answers,
        'comments_with_upvotes': comments_with_upvotes,
        'comments': comments  
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

        
@login_required(login_url='login')
def create_question(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()

            # Get or create the category
            category_name = request.POST.get('category')
            category, created = Category.objects.get_or_create(name=category_name)
            # Add the category to the question's categories using the set() method
            question.category.set([category])

            # Retrieve the tags data from the submitted form data
            tags = request.POST.get('tags')
            # Split the tags string into a list
            tag_list = tags.split(',')
            # Process and save the tags data to the database
            for tag_name in tag_list:
                tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                question.tags.add(tag)

            # Save the question again to update the many-to-many relationship
            question.save()
            return redirect('Questionlist')
    else:
        form = QuestionForm()
        
    context = {
        'form': form,
        'categories': categories 
    }
    return render(request, 'Forum/createquestion.html', context=context)



@login_required(login_url='login')
def update_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            updated_question = form.save(commit=False)
            updated_question.user = request.user
            updated_question.save()

            # Get or create the category
            category_name = request.POST.get('category')
            category, created = Category.objects.get_or_create(name=category_name)
            # Add the category to the question's categories using the set() method
            updated_question.category.set([category])

            # Retrieve the tags data from the submitted form data
            tags = request.POST.get('tags')
            # Split the tags string into a list
            tag_list = tags.split(',')
            # Process and save the tags data to the database
            updated_question.tags.clear()  # Clear existing tags
            for tag_name in tag_list:
                tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                updated_question.tags.add(tag)

            # Save the question again to update the many-to-many relationship
            updated_question.save()
            return redirect('home')
    else:
        form = QuestionForm(instance=question)
        
    context = {
        'form': form,
        'categories': categories,
        'question': question,
    }
    return render(request, 'Forum/updatequestion.html', context=context)
    


    

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



