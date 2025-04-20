from django.shortcuts import render, get_object_or_404
from .models import DiscussionThread, Comment, CommentVote
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Case, When, IntegerField
from django.http import FileResponse
from django.conf import settings
from django.contrib.auth.models import User
from .models import QuestionPaper
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
import json


def home(request):
    return render(request,'homepage.html')

def question_papers_list(request):
    papers_by_year = {
        '1st Year': QuestionPaper.objects.filter(year_of_study='1st Year'),
        '2nd Year': QuestionPaper.objects.filter(year_of_study='2nd Year'),
        '3rd Year': QuestionPaper.objects.filter(year_of_study='3rd Year'),
        '4th Year': QuestionPaper.objects.filter(year_of_study='4th Year'),
    }
    return render(request, 'pdfs.html', {'papers_by_year': papers_by_year})

def download_paper(request, pk):
    paper = get_object_or_404(QuestionPaper, pk=pk)
    return FileResponse(paper.file, as_attachment=True)

def papers_view(request):
    year = request.GET.get('year')
    branch = request.GET.get('branch')
    paper_year = request.GET.get('paper_year')
    search_query = request.GET.get('search', '')
    
    papers = QuestionPaper.objects.all()
    
    if year:
        papers = papers.filter(year_of_study=year)
    if branch and year != '1st':
        papers = papers.filter(branch=branch)
    if paper_year:
        papers = papers.filter(paper_year=paper_year)
    
    if search_query:
        papers = papers.filter(subject__icontains=search_query)
        
    paper_years = QuestionPaper.objects.values_list('paper_year', flat=True).distinct()
    
    context = {
        'papers': papers,
        'years': ['1st', '2nd', '3rd', '4th'],
        'branches': ['CSE', 'IT', 'Allied'],
        'paper_years': paper_years,
        'search_query': search_query,  # Pass search query back to template
    }
    return render(request, 'papers.html', context)

def get_filtered_papers(request):
    year = request.GET.get('year')
    branch = request.GET.get('branch')
    paper_year = request.GET.get('paper_year')

    papers = QuestionPaper.objects.all()

    if year:
        papers = papers.filter(year_of_study=year)

    if branch and year != "1st": 
        papers = papers.filter(branch=branch)

    if paper_year:
        papers = papers.filter(paper_year=paper_year)

    papers_data = []
    for paper in papers:
        papers_data.append({
            'subject': paper.subject,
            'file_url': paper.file.url,
        })

    return JsonResponse({'papers': papers_data})


def paper_detail(request, paper_id):
    paper = get_object_or_404(QuestionPaper, id=paper_id)
    thread, _ = DiscussionThread.objects.get_or_create(paper=paper)
    return render(request, 'paper_detail.html', {'paper_id': paper_id, 'paper': paper, 'thread': thread,  'current_user': request.user.username})


def get_all_users(username):
    users = User.objects.all()
    
    for user in users:
        if(username == user.username):
            return user.first_name
    return username

def get_comments(request, thread_id):
    thread = get_object_or_404(DiscussionThread, id=thread_id)
    # Get sort parameter
    sort_by = request.GET.get('sort', 'newest')
    comments = thread.comments.filter(parent__isnull=True)

    if sort_by == 'top':
        comments = comments.annotate(
        upvotes=Count(Case(When(votes__vote_type='upvote', then=1), output_field=IntegerField()))
    ).order_by('-upvotes', '-created_at')
    else:
        comments = comments.order_by('-created_at')

    
    comments_data = []
    
    for comment in comments:
        # Check if user has liked or disliked this comment
        user_liked = False
        user_disliked = False
        
        if request.user.is_authenticated:
            user_liked = CommentVote.objects.filter(
                comment=comment, 
                user=request.user, 
                vote_type='upvote'
            ).exists()
            
            user_disliked = CommentVote.objects.filter(
                comment=comment, 
                user=request.user, 
                vote_type='downvote'
            ).exists()
        
        # Get replies
        replies = comment.replies.all().order_by('created_at')
        replies_data = []
        
        for reply in replies:
            # Check if user has liked or disliked this reply
            reply_user_liked = False
            reply_user_disliked = False
            
            if request.user.is_authenticated:
                reply_user_liked = CommentVote.objects.filter(
                    comment=reply, 
                    user=request.user, 
                    vote_type='upvote'
                ).exists()
                
                reply_user_disliked = CommentVote.objects.filter(
                    comment=reply, 
                    user=request.user, 
                    vote_type='downvote'
                ).exists()
            reply_full_name = get_all_users(reply.user.username)
            replies_data.append({
                'id': reply.id,
                'content': reply.content,
                'user': reply.user.username,
                'full_name': reply_full_name,
                'created_at': reply.created_at.isoformat(),
                'upvote_count': reply.upvote_count(),
                'user_liked': reply_user_liked,
                'user_disliked': reply_user_disliked,
            })
        comment_full_name = get_all_users(comment.user.username)    
        comment_data = {
            'id': comment.id,
            'content': comment.content,
            'user': comment.user.username,
            'full_name': comment_full_name,
            'created_at': comment.created_at.isoformat(),
            'upvote_count': comment.upvote_count(),
            'user_liked': user_liked,
            'user_disliked': user_disliked,
            'replies': replies_data
        }
        
        comments_data.append(comment_data)
        
    return JsonResponse(comments_data, safe=False)


@csrf_exempt
@login_required
def post_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        thread_id = data.get('thread_id')
        content = data.get('content')
        parent_id = data.get('parent_id')

        if not content:
            return JsonResponse({"error": "Content cannot be empty."}, status=400)
            
        thread = get_object_or_404(DiscussionThread, id=thread_id)
        parent = None
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id, thread=thread)

        comment = Comment.objects.create(
            thread=thread, 
            user=request.user, 
            content=content, 
            parent=parent
        )
        
        return JsonResponse({"success": True, "comment_id": comment.id})

    return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
@login_required
def like_comment(request, comment_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            is_reply = data.get('is_reply', False)
            
            comment = get_object_or_404(Comment, id=comment_id)
            
            # Check if user has already voted
            existing_vote = CommentVote.objects.filter(
                comment=comment,
                user=request.user
            ).first()
            
            if existing_vote and existing_vote.vote_type == 'upvote':
                # User is toggling the upvote off
                existing_vote.delete()
                liked = False
            else:
                # Remove any existing vote (could be a downvote)
                if existing_vote:
                    existing_vote.delete()
                    
                # Create new upvote
                CommentVote.objects.create(
                    comment=comment,
                    user=request.user,
                    vote_type='upvote'
                )
                liked = True
                
            # Get updated likes count
            likes_count = CommentVote.objects.filter(
                comment=comment, 
                vote_type='upvote'
            ).count()
            
            return JsonResponse({
                'success': True, 
                'liked': liked,
                'likes_count': likes_count
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
@login_required
def dislike_comment(request, comment_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            is_reply = data.get('is_reply', False)
            
            comment = get_object_or_404(Comment, id=comment_id)
            
            # Check if user has already voted
            existing_vote = CommentVote.objects.filter(
                comment=comment,
                user=request.user
            ).first()
            
            if existing_vote and existing_vote.vote_type == 'downvote':
                # User is toggling the downvote off
                existing_vote.delete()
                disliked = False
            else:
                # Remove any existing vote (could be an upvote)
                if existing_vote:
                    existing_vote.delete()
                    
                # Create new downvote
                CommentVote.objects.create(
                    comment=comment,
                    user=request.user,
                    vote_type='downvote'
                )
                disliked = True
                
            # Get updated likes count
            likes_count = CommentVote.objects.filter(
                comment=comment, 
                vote_type='upvote'
            ).count()
            
            return JsonResponse({
                'success': True, 
                'disliked': disliked,
                'likes_count': likes_count
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
@login_required
def delete_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = get_object_or_404(Comment, id=comment_id)
            
            # Check if the user is the comment author
            if comment.user != request.user:
                return JsonResponse({'success': False, 'error': 'You are not authorized to delete this comment'})
                
            # Delete the comment
            comment.delete()
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'})